"""Coquille distante simulee pour le faux `ssh` (sessions interactives).

Le scenario de la mission decrit la machine cible (arborescence + flags).
Ici, petit shell realiste : ls, cd, pwd, cat, echo, whoami, id, exit.
"""

import datetime


class RemoteShell:
    def __init__(self, host_label, user, fs):
        # fs : dictionnaires imbriques (dossiers) / chaines (fichiers).
        self.host_label = host_label
        self.user = user
        self.fs = fs if isinstance(fs, dict) else {}
        home = ["home", user]
        self.cwd = home if self._exists_dir(home) else []

    # -- navigation ---------------------------------------------------
    def _node(self, parts):
        node = self.fs
        for part in parts:
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        return node

    def _exists_dir(self, parts):
        return isinstance(self._node(parts), dict)

    def _resolve(self, path):
        if path.startswith("/"):
            parts = []
            chunks = path.split("/")
        else:
            parts = list(self.cwd)
            chunks = path.split("/")
        for chunk in chunks:
            if chunk in ("", "."):
                continue
            if chunk == "..":
                if parts:
                    parts.pop()
                continue
            parts.append(chunk)
        return parts

    def _abspath(self, parts):
        return "/" + "/".join(parts)

    def _relpath(self):
        home = ["home", self.user]
        if self.cwd[:len(home)] == home:
            rest = self.cwd[len(home):]
            return "~" + ("/" + "/".join(rest) if rest else "")
        return self._abspath(self.cwd)

    # -- commandes ----------------------------------------------------
    def _cmd_ls(self, args):
        long = False
        show_all = False
        paths = []
        for arg in args:
            if arg.startswith("-"):
                if "l" in arg:
                    long = True
                if "a" in arg:
                    show_all = True
                continue
            paths.append(arg)
        target = self._resolve(paths[0]) if paths else list(self.cwd)
        node = self._node(target)
        if node is None:
            return "ls: cannot access '{}': No such file or directory".format(paths[0] if paths else "")
        if not isinstance(node, dict):
            return self._abspath(target)
        names = sorted(node.keys())
        if not show_all:
            names = [n for n in names if not n.startswith(".")]
        if not long:
            return "\n".join(names)
        lines = []
        stamp = datetime.date.today().strftime("%b %d %H:%M")
        for name in names:
            child = node[name]
            if isinstance(child, dict):
                lines.append("drwxr-xr-x 2 {} {} 4096 {} {}".format(self.user, self.user, stamp, name))
            else:
                size = len(str(child).encode("utf-8", "replace"))
                lines.append("-rw-r--r-- 1 {} {} {:>4} {} {}".format(self.user, self.user, size, stamp, name))
        return "\n".join(lines)

    def _cmd_cd(self, args):
        dest = args[0] if args else "/home/{}".format(self.user)
        if dest == "~":
            dest = "/home/{}".format(self.user)
        target = self._resolve(dest)
        node = self._node(target)
        if node is None:
            return "bash: cd: {}: No such file or directory".format(args[0] if args else "")
        if not isinstance(node, dict):
            return "bash: cd: {}: Not a directory".format(args[0])
        self.cwd = target
        return ""

    def _cmd_cat(self, args):
        if not args:
            return "cat: missing operand"
        out = []
        for arg in args:
            target = self._resolve(arg)
            node = self._node(target)
            if node is None:
                out.append("cat: {}: No such file or directory".format(arg))
            elif isinstance(node, dict):
                out.append("cat: {}: Is a directory".format(arg))
            else:
                out.append(str(node).rstrip("\n"))
        return "\n".join(o for o in out if o != "" or True).rstrip("\n")

    def _cmd_echo(self, line):
        # echo texte / echo texte > fichier / echo texte >> fichier
        body = line[4:].strip() if line.startswith("echo") else line
        append = " >> " in body
        if append:
            text, _, fname = body.partition(" >> ")
        elif " > " in body:
            text, _, fname = body.partition(" > ")
            fname = fname.strip()
        else:
            return self._unquote(body)
        fname = fname.strip()
        text = self._unquote(text.strip())
        target = self._resolve(fname)
        if not target:
            return "bash: {}: No such file or directory".format(fname)
        parent = self._node(target[:-1])
        if not isinstance(parent, dict):
            return "bash: {}: No such file or directory".format(fname)
        if append and target[-1] in parent and not isinstance(parent[target[-1]], dict):
            parent[target[-1]] = str(parent[target[-1]]) + text + "\n"
        else:
            parent[target[-1]] = text + "\n"
        return ""

    @staticmethod
    def _unquote(text):
        if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
            return text[1:-1]
        return text

    # -- boucle -------------------------------------------------------
    def execute(self, line):
        line = line.strip()
        if not line:
            return ""
        if line.startswith("echo"):
            return self._cmd_echo(line)
        parts = line.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "ls":
            return self._cmd_ls(args)
        if cmd == "cd":
            return self._cmd_cd(args)
        if cmd == "pwd":
            return self._abspath(self.cwd)
        if cmd == "cat":
            return self._cmd_cat(args)
        if cmd == "whoami":
            return self.user
        if cmd == "id":
            return "uid=1001({0}) gid=1001({0}) groups=1001({0})".format(self.user)
        if cmd == "hostname":
            return self.host_label
        if cmd in ("clear",):
            return "\n" * 40
        if cmd in ("help", "aide"):
            return "Commandes : ls cd pwd cat echo whoami id hostname clear exit"
        if cmd in ("exit", "logout", "quit"):
            return "__EXIT__"
        return "bash: {}: command not found".format(cmd)

    def run(self):
        short = self.host_label.replace(".", "-")
        while True:
            try:
                prompt = "{}@{}:{}$ ".format(self.user, short, self._relpath())
                line = input(prompt)
            except EOFError:
                print("logout")
                return
            result = self.execute(line)
            if result == "__EXIT__":
                print("logout")
                return
            if result:
                print(result, flush=True)
