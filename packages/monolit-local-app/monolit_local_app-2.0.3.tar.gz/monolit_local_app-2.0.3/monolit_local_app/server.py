from flask import Flask, Response, Request, send_file, jsonify, request
from monolit_local_app.funces import *
from typing import Callable

server = Flask(__name__)
path_to_build_ = None
path_to_index_ = None
process_request_ = None
process_path_ = None
communication_path_ = None

@server.route("/")
def send_index() -> tuple[Response | str, int]:
    """This fuction sends main index.html file"""

    try:
        return send_file(path_to_index_), 200
    except Exception as e:
        return e.__str__(), 404

@server.route("/<path:path>.<ext>")
def send_static(path: str, ext: str) -> tuple[Response | str, int]:
    """This function sends all requested static files"""
    
    path = process_path_(path) if isinstance(process_path_(path), str) else path

    try:
        return send_file(sum_paths(path_to_build_, f"{path}.{ext}")), 200
    except Exception as e:
        return e.__repr__(), 200

@server.route("/<path:path>")
def change_page(path: str) -> tuple[Response, int]:
    """This function change page of your application"""

    return send_file(path_to_index_), 200

def run(
    path_to_build: str | None,
    path_to_index: str | None,
    path_to_static: str | None,
    process_request: Callable[[Request], Response] | None = None,
    process_path: Callable[[str], str] | None = None,
    communication_path: str | None = "process",
    host: str | None = "127.0.0.1",
    port: int | None = 3000,
    debug: bool | None = False,
):
    """
    This function hosts your JavaScript project at the URL you specify.
    
    Args:
        path_to_build: Absolute path to build-folder
        path_to_index: Absolute path to file index.html
        path_to_static: Absolute path to static-folder
        process_request: Method for requests client
        process_path: Method for additional processing client's requested paths
        host: Url-address
        port: Number of port
        debug: Operating mode
    """

    global path_to_build_, path_to_index_, communication_path_, process_path_
 
    path_to_build_ = path_to_build
    path_to_index_ = path_to_index
    communication_path_ = communication_path

    process_path_ = process_path if process_path != None else lambda path: path
    process_request_ = process_request if process_request != None else lambda request: jsonify({}), 200

    @server.route("/" + communication_path_, methods=["POST"])
    def wrapper_process_request():
        """This function for requests client"""

        if request.method == "POST":
            if request.is_json:
                try:
                    return process_request_(request)
                except Exception as e:
                    print(f"[SERVER] Can not process JSON: {e.__repr__()}")
                    return jsonify({"msg": "Can not process JSON", "error": e.__repr__()}), 400
            else:
                print(f"[SERVER] Request must be in JSON format")
                return jsonify({"msg": "Request must be in JSON format"}), 415
        else:
            print(f"[SERVER] Method '{request.method}' not support")
            return jsonify({"msg": f"Method '{request.method}' not support"}), 405

    server.static_folder = path_to_static

    server.run(host, port, debug)

class LocalServer:
    """
    This class helps start local-server<br>
    Make your application class inherit from this class
    """

    def __init__(
        self,
        path_to_build: str | None,
        path_to_index: str | None,
        path_to_static: str | None,
        communication_path: str | None = "process",
        host: str | None = "127.0.0.1",
        port: int | None = 3000,
        debug: bool | None = False,
    ):
        """
        Initializes all properties
        
        Args:
            path_to_build: Absolute path to build-folder
            path_to_index: Absolute path to file index.html
            path_to_static: Absolute path to static-folder
            process_request: Method for requests client
            host: Url-address
            port: Number of port
            debug: Operating mode
        """

        self.path_to_build: str | None = path_to_build
        self.path_to_index: str | None = path_to_index
        self.path_to_static: str | None = path_to_static
        self.communication_path: str | None = communication_path
        self.host: str | None = host
        self.port: int | None = port
        self.debug: bool | None = debug

    def process_request(self, request: Request) -> Response:
        """
        <h2>For inheritance!</h2><br>
        This method should receive a <code>request</code> from the client and respond to it
        
        Args:
            request: client's request in json format

        Returns:
            Responce: answer on client-request
        """
    
    def process_path(self, path: str) -> str:
        """
        <h2>For inheritance!</h2><br>
        This method should receive a <code>path-to-file</code> from the client and process this path

        Args:
            path: client's path to some file

        Returns:
            str: alternative or same path
        """

    def __call__(self):
        """This function hosts your JavaScript project at the URL you specify. It is analog function run"""

        run(
            self.path_to_build,
            self.path_to_index,
            self.path_to_static,
            self.process_request,
            self.process_path,
            self.communication_path,
            self.host,
            self.port,
            self.debug
        )