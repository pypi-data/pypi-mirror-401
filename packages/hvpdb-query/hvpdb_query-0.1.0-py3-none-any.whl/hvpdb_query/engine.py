class QueryEngine:

    def __init__(self, db):
        self.db = db

    def execute(self, plan):
        if not plan:
            return None
        lang = plan.get('lang')
        
        try:
            if lang == 'sql':
                return self._exec_sql(plan)
            elif lang == 'mongo':
                return self._exec_mongo(plan)
            elif lang == 'redis':
                return self._exec_redis(plan)
            elif lang == 'cql':
                return self._exec_cql(plan)
            elif lang == 'dynamo':
                return self._exec_dynamo(plan)
            elif plan.get('type') == 'search':
                return 'Basic search not implemented in engine yet.'
        except Exception as e:
            return f"Execution Error ({lang}): {str(e)}"
            
        return None

    def _exec_sql(self, plan):
        op = plan['op']
        table = plan['table']
        if table not in self.db.get_all_groups():
            return f"Error: Table '{table}' not found."
        grp = self.db.group(table)
        
        if op == 'select':
            where = plan.get('where')
            query = self._parse_where(where)
            
            # Execute Find
            docs = grp.find(query)
            
            # 1. Sorting (ORDER BY)
            order_by = plan.get('order_by')
            if order_by:
                reverse = False
                key = order_by
                if order_by.lower().endswith(' desc'):
                    key = order_by[:-5].strip()
                    reverse = True
                elif order_by.lower().endswith(' asc'):
                    key = order_by[:-4].strip()
                    
                docs.sort(key=lambda x: x.get(key, 0), reverse=reverse)
            
            # 2. Offset
            offset = plan.get('offset')
            if offset:
                docs = docs[offset:]
                
            # 3. Limit
            limit = plan.get('limit')
            if limit:
                docs = docs[:limit]
            
            # 4. Field Selection
            fields = plan.get('fields')
            if fields and fields != '*':
                keys = [k.strip() for k in fields.split(',')]
                filtered_docs = []
                for d in docs:
                    new_d = {k: d.get(k) for k in keys if k in d}
                    filtered_docs.append(new_d)
                return filtered_docs
            return docs
            
        elif op == 'insert':
            data = plan.get('data')
            if data:
                res = grp.insert(data)
                self.db.commit()
                return f"Inserted 1 row. ID: {res['_id']}"
            return 'Insert failed: No data parsed.'
            
        elif op == 'delete':
            where = plan.get('where')
            query = self._parse_where(where)
            count = grp.delete(query)
            self.db.commit()
            return f'Deleted {count} documents.'
            
        elif op == 'update':
            where = plan.get('where')
            data = plan.get('data')
            if not data:
                return 'Error: No data to update (SET clause empty).'
            query = self._parse_where(where)
            count = grp.update(query, data)
            self.db.commit()
            return f'Updated {count} documents.'
            
        return 'Unknown SQL operation.'

    def _exec_mongo(self, plan):
        col_name = plan['collection']
        op = plan['op']
        args = plan['args']
        
        if col_name not in self.db.get_all_groups() and op != 'insert':
            return f"Error: Collection '{col_name}' not found."
            
        grp = self.db.group(col_name)
        
        if op == 'find':
            return grp.find(args)
        elif op == 'findOne':
            return grp.find_one(args)
        elif op == 'insert':
            res = grp.insert(args)
            self.db.commit()
            return res
        elif op == 'count':
            return grp.count()
        elif op in ('deleteOne', 'deleteMany'):
            count = grp.delete(args)
            self.db.commit()
            return {'deletedCount': count}
        elif op in ('updateOne', 'updateMany'):
            # Mongo update has (filter, update_ops)
            # HVPDB update is (filter, data_to_merge)
            # We assume simple merge for now
            count = grp.update(args, {}) # Need update data? Parser needs fix for 2 args
            # Limitation: Parser currently only grabs one JSON arg object.
            return "Update not fully supported in this version (requires 2 args)."
            
        return f"Mongo op '{op}' not supported."

    def _exec_redis(self, plan):
        grp = self.db.group('redis_kv')
        op = plan['op']
        
        # Key Operations
        if op == 'KEYS':
            pattern = plan.get('key', '*')
            # Simple prefix match if pattern ends with *
            all_keys = [d['_id'] for d in grp.find()]
            if pattern == '*': return all_keys
            if pattern.endswith('*'):
                prefix = pattern[:-1]
                return [k for k in all_keys if k.startswith(prefix)]
            return [k for k in all_keys if k == pattern]
            
        if op == 'DEL':
            key = plan['key']
            count = grp.delete({'_id': key})
            self.db.commit()
            return count
            
        if op == 'EXISTS':
            key = plan['key']
            return 1 if grp.find_one({'_id': key}) else 0

        # String Operations
        if op == 'GET':
            doc = grp.find_one({'_id': plan['key']})
            return doc.get('value') if doc else '(nil)'
            
        if op == 'SET':
            key = plan['key']
            val = plan.get('value')
            existing = grp.find_one({'_id': key})
            if existing:
                grp.update({'_id': key}, {'value': val, 'type': 'string'})
            else:
                grp.insert({'_id': key, 'value': val, 'type': 'string'})
            self.db.commit()
            return 'OK'
            
        # Hash Operations
        if op == 'HSET':
            key = plan['key']
            field = plan['field']
            val = plan['value']
            doc = grp.find_one({'_id': key})
            if not doc:
                doc = {'_id': key, 'type': 'hash', 'value': {}}
                grp.insert(doc)
            
            if not isinstance(doc.get('value'), dict):
                return "WRONGTYPE Operation against a key holding the wrong kind of value"
                
            doc['value'][field] = val
            grp.update({'_id': key}, {'value': doc['value']}) # Full replace of value dict
            self.db.commit()
            return 1
            
        if op == 'HGET':
            key = plan['key']
            field = plan['field']
            doc = grp.find_one({'_id': key})
            if not doc or not isinstance(doc.get('value'), dict):
                return '(nil)'
            return doc['value'].get(field, '(nil)')
            
        if op == 'HGETALL':
            key = plan['key']
            doc = grp.find_one({'_id': key})
            if not doc: return []
            if not isinstance(doc.get('value'), dict):
                 return "WRONGTYPE"
            # Flatten list
            res = []
            for k, v in doc['value'].items():
                res.extend([k, v])
            return res

        return None
        
    def _exec_cql(self, plan):
        op = plan['op']
        if op == 'truncate':
            table = plan['table']
            if table in self.db.get_all_groups():
                self.db.group(table).truncate()
                self.db.commit()
                return "TRUNCATED"
            return f"Table {table} not found."
        return "Unsupported CQL Op"

    def _exec_dynamo(self, plan):
        op = plan['op']
        import json
        
        table_name = plan.get('table-name')
        if not table_name: return "Missing --table-name"
        
        grp = self.db.group(table_name)
        
        if op == 'get-item':
            key_json = plan.get('key')
            if not key_json: return "Missing --key"
            try:
                # DynamoDB uses {"Key": {"S": "Value"}} format usually, simplified here to plain JSON
                key_dict = json.loads(key_json)
                # In HVPDB, we usually query by fields. If key is primary key...
                # We treat it as a filter
                res = grp.find_one(key_dict)
                return res if res else {}
            except Exception as e:
                return f"Error parsing key: {e}"
                
        elif op == 'put-item':
            item_json = plan.get('item')
            if not item_json: return "Missing --item"
            try:
                item_dict = json.loads(item_json)
                grp.insert(item_dict)
                self.db.commit()
                return "Metrics: {CapacityUnits: 1.0}"
            except Exception as e:
                 return f"Error parsing item: {e}"
                 
        elif op == 'scan':
            docs = grp.find()
            return {"Items": docs, "Count": len(docs)}

        return f"Dynamo Op '{op}' not supported."

    def _parse_where(self, where_clause):
        query = {}
        if not where_clause:
            return query
            
        # Very basic AND support: k=v AND k2=v2
        conditions = where_clause.split(' and ') # case sensitive split for now, parser lowercased it? No.
        # Parser didn't lowercase where clause content.
        
        # Try split by ' AND ' case insensitive
        import re
        parts = re.split(r'\s+AND\s+', where_clause, flags=re.IGNORECASE)
        
        for part in parts:
            if '=' in part:
                k, v = [x.strip() for x in part.split('=', 1)]
                
                # Check for LIKE (simple * wildcard)
                # Actually SQL uses LIKE operator, here we are inside the '=' check?
                # Parser needs to handle operators properly.
                # Currently parser just passes raw string.
                
                # Basic value cleanup
                if v.isdigit():
                    v = int(v)
                elif v.startswith("'") and v.endswith("'"):
                    v = v[1:-1]
                
                query[k] = v
        
        return query
