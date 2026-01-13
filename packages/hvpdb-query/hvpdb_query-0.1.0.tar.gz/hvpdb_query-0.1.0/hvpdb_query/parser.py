import re
import json
import shlex

class PolyglotParser:

    def parse(self, query: str):
        query = query.strip()
        if not query:
            return None
        
        # Determine language
        q_upper = query.upper()
        
        # SQL Detection
        if q_upper.startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER')):
            return self._parse_sql(query)
            
        # Mongo Detection
        elif query.startswith('db.'):
            return self._parse_mongo(query)
            
        # Redis Detection
        elif q_upper.split()[0] in ('GET', 'SET', 'DEL', 'KEYS', 'HGET', 'HSET', 'HGETALL', 'HDEL', 'EXISTS', 'LPUSH', 'RPUSH', 'LPOP', 'RPOP', 'LLEN', 'LRANGE'):
            return self._parse_redis(query)
            
        # Cassandra/CQL Detection (Simplified)
        elif q_upper.startswith(('DESCRIBE', 'USE', 'TRUNCATE')):
             # Usually overlaps with SQL, but some unique commands
             return self._parse_cql(query)
             
        # DynamoDB Detection (JSON-like payloads usually, but lets support simple CLI style)
        elif q_upper.startswith(('GET-ITEM', 'PUT-ITEM', 'SCAN', 'QUERY')):
             return self._parse_dynamo(query)
             
        # Fallback: Search syntax (k=v)
        else:
            if '=' in query:
                return {'type': 'search', 'query': query}
            return None

    def _parse_sql(self, query):
        q_lower = query.lower()
        
        # SELECT
        if q_lower.startswith('select'):
            # Improved regex to capture LIMIT, ORDER BY, OFFSET
            pattern = r'select\s+(.*?)\s+from\s+(\w+)(?:\s+where\s+(.*?))?(?:\s+order\s+by\s+(.*?))?(?:\s+limit\s+(\d+))?(?:\s+offset\s+(\d+))?$'
            match = re.match(pattern, query, re.IGNORECASE | re.DOTALL)
            if match:
                fields, table, where, order_by, limit, offset = match.groups()
                return {
                    'lang': 'sql', 
                    'op': 'select', 
                    'table': table, 
                    'fields': fields.strip(), 
                    'where': where.strip() if where else None,
                    'order_by': order_by.strip() if order_by else None,
                    'limit': int(limit) if limit else None,
                    'offset': int(offset) if offset else None
                }
                
        # DELETE
        elif q_lower.startswith('delete'):
            query_fixed = re.sub(r'delete\s+\*\s+from', 'delete from', query, flags=re.IGNORECASE)
            match = re.match(r'delete\s+from\s+(\w+)(?:\s+where\s+(.*))?', query_fixed, re.IGNORECASE)
            if match:
                table, where = match.groups()
                return {'lang': 'sql', 'op': 'delete', 'table': table, 'where': where.strip() if where else None}
                
        # UPDATE
        elif q_lower.startswith('update'):
            match = re.match(r'update\s+(\w+)\s+set\s+(.*?)(?:\s+where\s+(.*))?$', query, re.IGNORECASE)
            if match:
                table, sets, where = match.groups()
                data = self._parse_sql_assignments(sets)
                return {'lang': 'sql', 'op': 'update', 'table': table, 'data': data, 'where': where.strip() if where else None}
                
        # INSERT
        elif q_lower.startswith('insert'):
            # Support INSERT INTO table (c1, c2) VALUES (v1, v2)
            # AND INSERT INTO table JSON '{...}'
            
            # Check JSON format first
            match_json = re.match(r"insert\s+into\s+(\w+)\s+json\s+'(.*)'", query, re.IGNORECASE)
            if match_json:
                table, json_str = match_json.groups()
                try:
                    data = json.loads(json_str.replace("'", '"'))
                    return {'lang': 'sql', 'op': 'insert', 'table': table, 'data': data}
                except:
                    pass
            
            # Standard SQL VALUES format
            match_values = re.match(r"insert\s+into\s+(\w+)\s*\((.*?)\)\s*values\s*\((.*?)\)", query, re.IGNORECASE)
            if match_values:
                table, cols_str, vals_str = match_values.groups()
                cols = [c.strip() for c in cols_str.split(',')]
                # Very basic value parser (doesn't handle commas in strings well)
                vals = [self._clean_sql_value(v.strip()) for v in vals_str.split(',')]
                
                if len(cols) == len(vals):
                    data = dict(zip(cols, vals))
                    return {'lang': 'sql', 'op': 'insert', 'table': table, 'data': data}

        return None

    def _parse_mongo(self, query):
        match = re.match(r'db\.(\w+)\.(\w+)\((.*)\)', query)
        if match:
            collection, op, args = match.groups()
            arg_data = {}
            if args.strip():
                try:
                    # Try to be lenient with JSON (allow single quotes)
                    # This is a naive replacement, but works for simple cases
                    valid_json = args
                    if "'" in valid_json and '"' not in valid_json:
                         valid_json = valid_json.replace("'", '"')
                    arg_data = json.loads(valid_json)
                except:
                    # If JSON parsing fails, try to return raw string if it's simple
                    pass
            return {'lang': 'mongo', 'collection': collection, 'op': op, 'args': arg_data}
        return None

    def _parse_redis(self, query):
        parts = shlex.split(query)
        if not parts:
            return None
        op = parts[0].upper()
        cmd = {'lang': 'redis', 'op': op}
        
        if len(parts) > 1:
            cmd['key'] = parts[1]
        
        if len(parts) > 2:
            if op == 'SET':
                cmd['value'] = parts[2]
            elif op == 'HSET':
                cmd['field'] = parts[2]
                if len(parts) > 3:
                    cmd['value'] = parts[3]
            elif op in ('HGET', 'HDEL', 'HEXISTS'):
                cmd['field'] = parts[2]
            elif op in ('LPUSH', 'RPUSH'):
                cmd['values'] = parts[2:]
                
        return cmd

    def _parse_cql(self, query):
        # CQL is very similar to SQL, but let's handle TRUNCATE specifically
        q_upper = query.upper()
        if q_upper.startswith('TRUNCATE'):
            match = re.match(r'truncate\s+(\w+)', query, re.IGNORECASE)
            if match:
                return {'lang': 'cql', 'op': 'truncate', 'table': match.group(1)}
        return None

    def _parse_dynamo(self, query):
        # Mock DynamoDB CLI syntax: get-item --table-name Music --key '{"Artist": "No One"}'
        parts = shlex.split(query)
        op = parts[0].lower()
        cmd = {'lang': 'dynamo', 'op': op}
        
        # Simple arg parsing
        it = iter(parts[1:])
        for arg in it:
            if arg.startswith('--'):
                key = arg[2:]
                try:
                    val = next(it)
                    cmd[key] = val
                except StopIteration:
                    pass
        return cmd

    def _parse_sql_assignments(self, sets_str):
        data = {}
        for assignment in sets_str.split(','):
            if '=' in assignment:
                k, v = [x.strip() for x in assignment.split('=', 1)]
                data[k] = self._clean_sql_value(v)
        return data

    def _clean_sql_value(self, v):
        if v.isdigit():
            return int(v)
        elif v.replace('.', '', 1).isdigit():
            return float(v)
        elif v.startswith("'") and v.endswith("'"):
            return v[1:-1]
        elif v.lower() == 'true':
            return True
        elif v.lower() == 'false':
            return False
        elif v.lower() == 'null':
            return None
        return v
