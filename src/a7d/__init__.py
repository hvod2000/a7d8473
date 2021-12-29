import a7d.encoder
import a7d.decoder
import pathlib


class Archive:
    def __init__(self, content):
        if isinstance(content, Archive):
            content = content.content
        elif not isinstance(content, dict):
            content = Archive.load(content).content
        self.content = content

    def __repr__(self):
        return f"Archive({self.content})"

    def to_bytes(self):
        return b"a7d8473\n" + encoder.encode_nodes(self.content)

    def save(self, path):
        return pathlib.Path(path).write_bytes(self.to_bytes())

    def to_directory(self, dir_path):
        return write_directory(dir_path, self.content)

    def iterdir(self):
        yield from ((n.decode(), Archive(c)) for n, c in self.content.items())

    @staticmethod
    def from_bytes(bts):
        assert bts[:8] == b"a7d8473\n"
        return Archive(decoder.decode_nodes(bts[8:])[0])

    @staticmethod
    def from_directory(dir_path):
        name, nodes = read_directory(dir_path)
        return Archive(nodes)

    @staticmethod
    def load(path):
        path = pathlib.Path(path)
        if path.is_dir():
            return Archive.from_directory(path)
        return Archive.from_bytes(path.read_bytes())


def write_node(path, content):
    path = pathlib.Path(path)
    if isinstance(content, dict):
        return write_directory(path, content)
    t, content = content
    if t == "l":
        return path.symlink_to(content[:-1])
    path.write_bytes(content)
    path.chmod(path.stat().st_mode | (73 * (t == "x")))


def write_directory(path, nodes):
    path = pathlib.Path(path)
    path.mkdir(parents=True, exist_ok=True)
    for name, node in nodes.items():
        write_node(path / name.decode(), node)


def read_node(path):
    path = pathlib.Path(path)
    if path.is_dir():
        return read_directory(path)
    content = bytes(path.readlink()) if path.is_symlink() else path.read_bytes()
    t = "l" if path.is_symlink() else "-x"[(path.stat().st_mode >> 6) & 1]
    return path.name.encode(), (t, content + b"\n" * (t == "l"))


def read_directory(path):
    path = pathlib.Path(path)
    nodes = dict(read_node(p) for p in path.iterdir())
    return (path.name.encode(), nodes)
