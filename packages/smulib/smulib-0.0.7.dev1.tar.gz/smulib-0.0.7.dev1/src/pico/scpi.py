import sys

from serial_helper import write_line


def _split_cmd(cmd_line: str):
    cmd_line = cmd_line.strip()
    if not cmd_line:
        return ([], False, [])

    is_query = cmd_line.endswith('?')
    # separate possible parameters after a space (SCPI often uses space or comma)
    # example: "MEAS:VOLT 5,2" or "CONF:VOLT 5"
    parts = cmd_line.split(None, 1)  # split into command and rest
    cmd_part = parts[0].upper()
    params_part = parts[1] if len(parts) > 1 else ''

    # remove trailing '?' from last token if is_query
    if is_query:
        cmd_part = cmd_part[:-1] if cmd_part.endswith('?') else cmd_part

    # split hierarchical: e.g. "MEAS:VOLT"
    path = [p for p in cmd_part.split(':') if p != '']
    # params: split by comma and strip
    params = [p.strip() for p in params_part.split(',')] if params_part else []
    # convert empty strings to []
    if params == ['']:
        params = []
    return (path, is_query, params)

def _try_number(s):
    try:
        if '.' in s:
            return float(s)
        else:
            return int(s)
    except Exception:
        return s

# SCPI Processor core -------------------------------------------------------

class SCPIError(Exception):
    def __init__(self, code=100, message='Undefined error'):
        self.code = code
        self.message = message
        super().__init__(f'{code},{message}')

class SCPIProcessor:
    def __init__(self):
        #   '_handler' -> function
        #   '_query' -> function
        #   subcommand -> nested dict
        self._tree = {}
        # transport functions
        # simple error queue
        self._errors = []
        # IDN default
        self.idn = 'TU Delft,PicoSMU,42069,0.1.0'
        # default system status
        self.status = 'OK'

        # register built-in commands
        self._register_builtin_commands()

    # -------------------- registration API --------------------

    def register(self, command_path, handler=None, query=None, replace=False):
        if isinstance(command_path, str):
            parts = [p for p in command_path.upper().split(':') if p != '']
        else:
            parts = [p.upper() for p in command_path]

        node = self._tree
        for p in parts:
            node = node.setdefault(p, {})
        if handler is not None:
            if not replace and '_handler' in node:
                raise SCPIError(200, 'Handler exists')
            node['_handler'] = handler
        if query is not None:
            if not replace and '_query' in node:
                raise SCPIError(201, 'Query handler exists')
            node['_query'] = query

    def query(self, command_path):
        def deco(f):
            self.register(command_path, query=f)
            return f
        return deco

    def command(self, command_path):
        def deco(f):
            self.register(command_path, handler=f)
            return f
        return deco

    # -------------------- built-in commands --------------------

    def _register_builtin_commands(self):
        # *IDN?
        self.register('*IDN', query=lambda p: self.idn)
        # *RST
        def rst_handler(params):
            # user can override or extend with own reset
            self._errors.clear()
            self.status = 'OK'
            return None
        self.register('*RST', handler=rst_handler)
        # SYST:ERR?
        def syst_err_query(params):
            if not self._errors:
                return '0,No error'
            else:
                e = self._errors.pop(0)
                return '{},{}'.format(e.get('code', -1), e.get('msg', 'Unknown'))
        self.register('SYST:ERR', query=syst_err_query)
        # SYST:STAT?
        self.register('SYST:STAT', query=lambda p: self.status)

    # -------------------- parsing + dispatch --------------------

    def _find_node(self, path):
        node = self._tree
        for p in path:
            if p not in node:
                return None
            node = node[p]
        return node

    def _dispatch(self, path, is_query, params):
        node = self._find_node(path)
        if node is None:
            raise SCPIError(104, 'Command error')  # 104 common SCPI for undefined header
        if is_query:
            q = node.get('_query')
            if q is None:
                raise SCPIError(107, 'Query not implemented')
            return q(params)
        else:
            h = node.get('_handler')
            if h is None:
                raise SCPIError(109, 'Command not implemented')
            return h(params)

    def handle_line(self, line):
        if not line:
            return None
        path, is_query, raw_params = _split_cmd(line)
        if not path:
            return None
        # convert params to numbers when possible
        params = [_try_number(p) for p in raw_params]
        try:
            resp = self._dispatch(path, is_query, params)
            # If handler returns tuple (code, message) treat as error
            if isinstance(resp, tuple) and len(resp) == 2 and isinstance(resp[0], int):
                # push error and return None (SCPI typically stores in queue)
                self._errors.append({'code': resp[0], 'msg': resp[1]})
                return None
            # If response is None -> no immediate output
            if resp is None:
                return None
            # otherwise string or convertible
            if not isinstance(resp, str):
                resp = str(resp)
            return resp
        except SCPIError as e:
            # push error into error queue and return standard SCPI error text optionally
            self._errors.append({'code': e.code, 'msg': e.message})
            # Many SCPI devices do not echo errors immediately; we'll return an error indicator optionally
            return None
        except Exception as e:
            # unexpected error
            self._errors.append({'code': 999, 'msg': str(e)})
            return None

    # -------------------- convenience helpers --------------------

    def add_error(self, code, msg):
        self._errors.append({'code': code, 'msg': msg})

    def list_commands(self):
        """Return a JSON-ish description of the registered commands (for debug)."""
        def walk(node, path):
            out = []
            for k, v in node.items():
                if k.startswith('_'):
                    continue
                sub = node[k]
                item = {'path': ':'.join(path + [k])}
                if '_handler' in sub:
                    item['has_handler'] = True
                if '_query' in sub:
                    item['has_query'] = True
                out.append(item)
                out += walk(sub, path + [k])
            return out
        return walk(self._tree, [])