import asyncio
import json
import logging
import os
import re
import sys
from pathlib import Path
from mysql.connector import connect, Error
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from pydantic import AnyUrl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_mysql_server")

# SQL statements that are allowed in read-only mode
READONLY_ALLOWED_PATTERNS = [
    r'^\s*SELECT\s+',
    r'^\s*SHOW\s+',
    r'^\s*DESCRIBE\s+',
    r'^\s*DESC\s+',
    r'^\s*EXPLAIN\s+',
    r'^\s*USE\s+',
]

# SQL statements that are explicitly forbidden in read-only mode
READONLY_FORBIDDEN_PATTERNS = [
    r'^\s*INSERT\s+',
    r'^\s*UPDATE\s+',
    r'^\s*DELETE\s+',
    r'^\s*DROP\s+',
    r'^\s*CREATE\s+',
    r'^\s*ALTER\s+',
    r'^\s*TRUNCATE\s+',
    r'^\s*REPLACE\s+',
    r'^\s*GRANT\s+',
    r'^\s*REVOKE\s+',
    r'^\s*LOCK\s+',
    r'^\s*UNLOCK\s+',
    r'^\s*CALL\s+',  # Stored procedures might modify data
    r'^\s*LOAD\s+',
    r'^\s*IMPORT\s+',
    r'^\s*RENAME\s+',
    r'^\s*SET\s+',  # Could change session variables
    r'^\s*START\s+TRANSACTION',
    r'^\s*BEGIN\s*',
    r'^\s*COMMIT\s*',
    r'^\s*ROLLBACK\s*',
]


def is_query_allowed_readonly(query: str) -> tuple[bool, str]:
    """
    Check if a query is allowed in read-only mode.
    Returns (is_allowed, reason).
    """
    query_upper = query.upper().strip()
    
    # Check forbidden patterns first
    for pattern in READONLY_FORBIDDEN_PATTERNS:
        if re.match(pattern, query_upper, re.IGNORECASE):
            return False, f"Query type not allowed in read-only mode: {query_upper.split()[0]}"
    
    # Check if it matches allowed patterns
    for pattern in READONLY_ALLOWED_PATTERNS:
        if re.match(pattern, query_upper, re.IGNORECASE):
            return True, ""
    
    # Default: deny unknown query types in read-only mode
    return False, f"Unknown query type not allowed in read-only mode: {query_upper.split()[0] if query_upper else 'empty'}"


class DatabaseConnection:
    """Represents a single database connection configuration that can access multiple databases."""
    
    def __init__(self, name: str, config: dict):
        """
        Initialize a database connection.
        
        Args:
            name: Connection name (used as tool name suffix)
            config: Connection configuration dict
        """
        self.name = name
        self.readonly = config.get("readonly", False)  # Read-only mode flag
        
        # Store allowed databases list (if specified)
        self.allowed_databases: list[str] = []
        databases = config.get("databases")
        if databases and isinstance(databases, list):
            self.allowed_databases = databases
        
        # Default database (first in list, or single database config)
        default_db = config.get("database")
        if not default_db and self.allowed_databases:
            default_db = self.allowed_databases[0]
        
        self.default_database = default_db
        
        self.config = {
            "host": config.get("host", "localhost"),
            "port": int(config.get("port", 3306)),
            "user": config.get("user"),
            "password": config.get("password"),
            "database": default_db,
            "charset": config.get("charset", "utf8mb4"),
            "collation": config.get("collation", "utf8mb4_unicode_ci"),
            "autocommit": True,
            "sql_mode": config.get("sql_mode", "TRADITIONAL")
        }
        # Remove None values
        self.config = {k: v for k, v in self.config.items() if v is not None}
        
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        required = ["user", "password"]
        # Need either a default database or a list of allowed databases
        has_database = self.config.get("database") or len(self.allowed_databases) > 0
        return all(self.config.get(k) for k in required) and has_database
    
    def get_connection(self, database: str | None = None):
        """
        Create and return a database connection.
        
        Args:
            database: Optional database name to connect to. If not specified, uses default.
        """
        conn_config = self.config.copy()
        if database:
            conn_config["database"] = database
        return connect(**conn_config)
    
    def is_readonly(self) -> bool:
        """Check if this connection is in read-only mode."""
        return self.readonly
    
    def get_default_database(self) -> str:
        """Get the default database name for this connection."""
        return self.default_database or "unknown"
    
    def get_allowed_databases(self) -> list[str]:
        """Get list of allowed databases. Empty list means any database is allowed."""
        return self.allowed_databases
    
    def is_database_allowed(self, database: str) -> bool:
        """Check if a database is allowed for this connection."""
        # If no restrictions, allow all
        if not self.allowed_databases:
            return True
        return database in self.allowed_databases
    
    def get_databases_description(self) -> str:
        """Get a description of available databases."""
        if self.allowed_databases:
            return ", ".join(self.allowed_databases)
        return self.default_database or "any"


class MultiDatabaseManager:
    """Manages multiple database connections."""
    
    def __init__(self):
        self.connections: dict[str, DatabaseConnection] = {}
        self._load_connections()
    
    def _load_connections(self):
        """Load database connections from config file or environment variables."""
        # Try to load from config file first
        config_path = os.getenv("MYSQL_CONFIG_FILE")
        if config_path and Path(config_path).exists():
            self._load_from_file(config_path)
        
        # Also try to load from JSON environment variable
        config_json = os.getenv("MYSQL_CONNECTIONS")
        if config_json:
            self._load_from_json(config_json)
        
        # Fallback: load single connection from legacy environment variables
        if not self.connections:
            self._load_legacy_config()
        
        logger.info(f"Loaded {len(self.connections)} database connection(s): {list(self.connections.keys())}")
    
    def _load_from_file(self, config_path: str):
        """Load connections from a JSON config file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            connections = config.get("connections", {})
            for name, conn_config in connections.items():
                self._load_connection(name, conn_config, "config file")
        except Exception as e:
            logger.error(f"Failed to load config file {config_path}: {e}")
    
    def _load_connection(self, name: str, conn_config: dict, source: str):
        """
        Load a single connection configuration.
        
        Args:
            name: Connection name
            conn_config: Connection configuration dict
            source: Source description for logging
        """
        if name in self.connections:
            return
        
        conn = DatabaseConnection(name, conn_config)
        if conn.validate():
            self.connections[name] = conn
            mode = "read-only" if conn.is_readonly() else "read-write"
            db_info = conn.get_databases_description()
            logger.info(f"Loaded connection '{name}' from {source} ({mode} mode, databases: {db_info})")
        else:
            logger.warning(f"Connection '{name}' missing required configuration, skipped")
    
    def _load_from_json(self, config_json: str):
        """Load connections from JSON string in environment variable."""
        try:
            config = json.loads(config_json)
            connections = config.get("connections", config)  # Support both formats
            for name, conn_config in connections.items():
                self._load_connection(name, conn_config, "environment variable")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MYSQL_CONNECTIONS JSON: {e}")
    
    def _load_legacy_config(self):
        """Load single connection from legacy environment variables for backward compatibility."""
        # Check for read-only mode: MYSQL_READONLY=true/1/yes
        readonly_env = os.getenv("MYSQL_READONLY", "").lower()
        readonly = readonly_env in ("true", "1", "yes")
        
        config = {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": os.getenv("MYSQL_PORT", "3306"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": os.getenv("MYSQL_DATABASE"),
            "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),
            "collation": os.getenv("MYSQL_COLLATION", "utf8mb4_unicode_ci"),
            "sql_mode": os.getenv("MYSQL_SQL_MODE", "TRADITIONAL"),
            "readonly": readonly
        }
        
        conn = DatabaseConnection("default", config)
        if conn.validate():
            self.connections["default"] = conn
            mode = "read-only" if readonly else "read-write"
            logger.info(f"Loaded default connection from legacy environment variables ({mode} mode)")
        else:
            logger.warning("No valid database configuration found")
    
    def get_connection(self, name: str) -> DatabaseConnection | None:
        """Get a database connection by name."""
        return self.connections.get(name)
    
    def list_connections(self) -> list[str]:
        """List all available connection names."""
        return list(self.connections.keys())


# Initialize server and database manager
app = Server("mcp-mysql-server")
db_manager = MultiDatabaseManager()


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List MySQL tables as resources for all connections and their databases."""
    resources = []
    
    for conn_name in db_manager.list_connections():
        db_conn = db_manager.get_connection(conn_name)
        if not db_conn:
            continue
        
        # Get list of databases to enumerate
        databases = db_conn.get_allowed_databases()
        if not databases:
            # If no specific databases configured, use the default
            databases = [db_conn.get_default_database()]
        
        for db_name in databases:
            try:
                logger.info(f"Listing tables for connection '{conn_name}', database '{db_name}'")
                with db_conn.get_connection(database=db_name) as conn:
                    logger.info(f"Connected to {conn_name}/{db_name}: MySQL server version {conn.get_server_info()}")
                    with conn.cursor() as cursor:
                        cursor.execute("SHOW TABLES")
                        tables = cursor.fetchall()
                        logger.info(f"Found {len(tables)} tables in '{conn_name}/{db_name}'")
                        
                        for table in tables:
                            resources.append(
                                Resource(
                                    uri=f"mysql://{conn_name}/{db_name}/{table[0]}/data",
                                    name=f"[{conn_name}:{db_name}] {table[0]}",
                                    mimeType="text/plain",
                                    description=f"Table '{table[0]}' in database '{db_name}' via connection '{conn_name}'"
                                )
                            )
            except Error as e:
                logger.error(f"Failed to list tables for '{conn_name}/{db_name}': {e}")
                if hasattr(e, 'errno'):
                    logger.error(f"Error code: {e.errno}, SQL state: {e.sqlstate}")
    
    return resources


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read table contents from a specific connection and database."""
    uri_str = str(uri)
    logger.info(f"Reading resource: {uri_str}")
    
    if not uri_str.startswith("mysql://"):
        raise ValueError(f"Invalid URI scheme: {uri_str}")
    
    # Parse URI: mysql://{connection_name}/{database}/{table}/data
    parts = uri_str[8:].split('/')
    if len(parts) < 3:
        raise ValueError(f"Invalid URI format: {uri_str}. Expected: mysql://connection/database/table/data")
    
    conn_name = parts[0]
    db_name = parts[1]
    table = parts[2]
    
    db_conn = db_manager.get_connection(conn_name)
    if not db_conn:
        raise ValueError(f"Unknown database connection: {conn_name}")
    
    # Check if database is allowed
    if not db_conn.is_database_allowed(db_name):
        raise ValueError(f"Database '{db_name}' is not allowed for connection '{conn_name}'")
    
    try:
        logger.info(f"Reading table '{table}' from connection '{conn_name}', database '{db_name}'")
        with db_conn.get_connection(database=db_name) as conn:
            logger.info(f"Connected to MySQL server version: {conn.get_server_info()}")
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [",".join(map(str, row)) for row in rows]
                return "\n".join([",".join(columns)] + result)
    except Error as e:
        logger.error(f"Database error reading resource {uri}: {e}")
        if hasattr(e, 'errno'):
            logger.error(f"Error code: {e.errno}, SQL state: {e.sqlstate}")
        raise RuntimeError(f"Database error: {e}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MySQL tools - one execute_sql tool per connection."""
    logger.info("Listing tools...")
    tools = []
    
    for conn_name in db_manager.list_connections():
        db_conn = db_manager.get_connection(conn_name)
        if not db_conn:
            continue
        
        # Create a unique tool for each database connection
        tool_name = f"execute_sql" if conn_name == "default" else f"execute_sql_{conn_name}"
        
        # Build description based on connection settings
        mode_str = " [READ-ONLY]" if db_conn.is_readonly() else ""
        db_info = db_conn.get_databases_description()
        
        if conn_name == "default":
            description = f"Execute an SQL query on the MySQL server (databases: {db_info}){mode_str}"
        else:
            description = f"Execute an SQL query on '{conn_name}' MySQL server (databases: {db_info}){mode_str}"
        
        # Adjust query description for read-only mode
        query_description = "The SQL query to execute"
        if db_conn.is_readonly():
            query_description = "The SQL query to execute (SELECT, SHOW, DESCRIBE, EXPLAIN only - read-only mode)"
        
        # Build database parameter description
        allowed_dbs = db_conn.get_allowed_databases()
        if allowed_dbs:
            db_param_description = f"Target database name. Allowed: {', '.join(allowed_dbs)}"
        else:
            db_param_description = f"Target database name (default: {db_conn.get_default_database()})"
        
        tools.append(
            Tool(
                name=tool_name,
                description=description,
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": query_description
                        },
                        "database": {
                            "type": "string",
                            "description": db_param_description
                        }
                    },
                    "required": ["query"]
                }
            )
        )
    
    logger.info(f"Listed {len(tools)} tools: {[t.name for t in tools]}")
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute SQL commands on the appropriate database connection."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    # Determine which connection to use based on tool name
    if name == "execute_sql":
        conn_name = "default"
    elif name.startswith("execute_sql_"):
        conn_name = name[len("execute_sql_"):]
    else:
        raise ValueError(f"Unknown tool: {name}")
    
    db_conn = db_manager.get_connection(conn_name)
    if not db_conn:
        raise ValueError(f"Unknown database connection: {conn_name}")
    
    query = arguments.get("query")
    if not query:
        raise ValueError("Query is required")
    
    # Get target database (optional, defaults to connection's default database)
    database = arguments.get("database")
    if database:
        # Validate database is allowed
        if not db_conn.is_database_allowed(database):
            allowed = db_conn.get_allowed_databases()
            return [TextContent(type="text", text=f"Error: Database '{database}' is not allowed for this connection. Allowed databases: {', '.join(allowed)}")]
    else:
        database = db_conn.get_default_database()
    
    # Check read-only mode restrictions
    if db_conn.is_readonly():
        is_allowed, reason = is_query_allowed_readonly(query)
        if not is_allowed:
            logger.warning(f"Query blocked by read-only mode on '{conn_name}': {reason}")
            return [TextContent(type="text", text=f"Error: {reason}. This connection is in read-only mode.")]
    
    try:
        logger.info(f"Executing query on '{conn_name}/{database}': {query[:100]}...")
        with db_conn.get_connection(database=database) as conn:
            logger.info(f"Connected to MySQL server version: {conn.get_server_info()}")
            with conn.cursor() as cursor:
                cursor.execute(query)
                
                # Special handling for SHOW TABLES
                if query.strip().upper().startswith("SHOW TABLES"):
                    tables = cursor.fetchall()
                    result = [f"Tables_in_{database}"]
                    result.extend([table[0] for table in tables])
                    return [TextContent(type="text", text="\n".join(result))]
                
                # Handle all other queries that return result sets
                elif cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    try:
                        rows = cursor.fetchall()
                        result = [",".join(map(str, row)) for row in rows]
                        return [TextContent(type="text", text="\n".join([",".join(columns)] + result))]
                    except Error as e:
                        logger.warning(f"Error fetching results: {e}")
                        return [TextContent(type="text", text=f"Query executed but error fetching results: {e}")]
                
                # Non-SELECT queries
                else:
                    conn.commit()
                    return [TextContent(type="text", text=f"Query executed successfully. Rows affected: {cursor.rowcount}")]
    
    except Error as e:
        logger.error(f"Error executing SQL '{query}': {e}")
        if hasattr(e, 'errno'):
            logger.error(f"Error code: {e.errno}, SQL state: {e.sqlstate}")
        return [TextContent(type="text", text=f"Error executing query: {e}")]


async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    # Print configuration info
    print("Starting MySQL MCP server...", file=sys.stderr)
    print(f"Loaded connections: {db_manager.list_connections()}", file=sys.stderr)
    
    for conn_name in db_manager.list_connections():
        db_conn = db_manager.get_connection(conn_name)
        if db_conn:
            mode = "[RO]" if db_conn.is_readonly() else "[RW]"
            db_info = db_conn.get_databases_description()
            print(f"  - {conn_name} {mode}: {db_conn.config.get('host')}:{db_conn.config.get('port')} (databases: {db_info})", file=sys.stderr)
    
    logger.info("Starting MySQL MCP server...")
    
    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            raise


if __name__ == "__main__":
    asyncio.run(main())
