import docker
from google.cloud import artifactregistry_v1
import json
import os


curr_dir = os.path.dirname(os.path.abspath(__file__))


def _get_app_list(project_id="repositories-368911", location="europe-southwest1"):
    # Initialize clients
    ar_client = artifactregistry_v1.ArtifactRegistryClient()

    # 1. Define the parent path for the region
    parent = f"projects/{project_id.strip()}/locations/{location}"

    # 2. List all repositories in that location
    repos_request = artifactregistry_v1.ListRepositoriesRequest(parent=parent)
    repos = ar_client.list_repositories(request=repos_request)

    tags = []

    for repo in repos:
        if repo.format_ == artifactregistry_v1.Repository.Format.DOCKER:
            # 3. List "packages" (the actual images) inside the repository
            # repo.name looks like: projects/PROJ/locations/LOC/repositories/REPO
            pkg_request = artifactregistry_v1.ListPackagesRequest(parent=repo.name)
            packages = ar_client.list_packages(request=pkg_request)

            # The hostname for Artifact Registry
            registry_host = f"{location}-docker.pkg.dev"
            repo_id = repo.name.split("/")[-1]

            # TODO: Remove this hack used during testing
            if repo_id == "acellera-docker-apps":
                continue

            for pkg in packages:
                # Get the image name (last part of the package resource name)
                image_name = pkg.name.split("/")[-1]

                # Full remote path: europe-southwest1-docker.pkg.dev/my-proj/my-repo/my-image
                remote_tag = (
                    f"{registry_host}/{project_id}/{repo_id}/{image_name}:latest"
                )
                tags.append(remote_tag)

    return tags


def update_docker_apps_from_gcloud(
    project_id="repositories-368911", location="europe-southwest1"
):
    from docker import from_env

    docker_client = from_env()

    tags = _get_app_list(project_id, location)
    for tag in tags:
        try:
            print(f"Pulling: {tag} ...")
            docker_client.images.pull(tag)
        except Exception as e:
            print(f"Failed to pull {tag}: {e}")


def _get_app_manifests(prefix):
    """
    Finds local images starting with prefix, runs them to dump a manifest,
    and returns a dictionary of the manifest contents.
    """
    import tempfile
    from pathlib import Path

    client = docker.from_env()

    # 1. Filter local images by prefix
    # We look for tags that start with the prefix (e.g., 'pm-my-app:latest')
    target_images = []
    for img in client.images.list():
        for tag in img.tags:
            if "acellera-docker-apps" in tag:
                continue  # TODO: Remove this hack used during testing
            if tag.startswith(prefix):
                target_images.append(tag)

    manifests = {}

    for image_tag in target_images:
        print(f"--- Processing: {image_tag} ---")

        # 2. Setup temporary host directory for mounting
        with tempfile.TemporaryDirectory() as tmp_dir:
            host_path = Path(tmp_dir)
            container_manifest_dir = "/manifest"
            filename = "manifest.json"

            try:
                # 3. Run the container
                # command: The argument to pass to the entrypoint
                # volumes: Bind mount the temp dir to /manifest
                # remove: Clean up the container immediately after exit
                client.containers.run(
                    image=image_tag,
                    command=f"--dump-manifest {container_manifest_dir}/{filename}",
                    volumes={
                        str(host_path.resolve()): {
                            "bind": container_manifest_dir,
                            "mode": "rw",
                        },
                        "/etc/passwd": {"bind": "/etc/passwd", "mode": "ro"},
                        "/etc/group": {"bind": "/etc/group", "mode": "ro"},
                    },
                    remove=True,
                    user=f"{os.getuid()}:{os.getgid()}",
                    extra_hosts={"host.docker.internal": "host-gateway"},
                    environment={
                        "ACELLERA_LICENCE_SERVER": "27000@host.docker.internal",
                    },
                )

                # 4. Read the file from the host's temp directory
                manifest_file = host_path / filename
                if manifest_file.exists():
                    with open(manifest_file, "r") as f:
                        manifests[image_tag] = json.load(f)
                else:
                    raise RuntimeError(f"No manifest file found for {image_tag}")

            except Exception as e:
                raise RuntimeError(f"Failed to run {image_tag}: {e}")

    return manifests


def _get_apps(project_id="repositories-368911", location="europe-southwest1"):
    cache_folder = os.path.join(os.path.expanduser("~"), ".cache", "playmolecule")
    os.makedirs(cache_folder, exist_ok=True)

    prefix = f"{location}-docker.pkg.dev/{project_id}"
    manifests = _get_app_manifests(prefix)
    apps = {}

    for image_tag, manifest in manifests.items():
        container_config = manifest["container_config"]
        app_name = container_config["name"].lower()
        version = container_config["version"]

        with open(os.path.join(curr_dir, "share", "docker_run.sh"), "r") as f:
            run_sh = f.read()

        run_sh = run_sh.replace("{docker_container_name}", f'"{image_tag}"')

        cache_run_sh = os.path.join(cache_folder, f"run_{app_name}_{version}.sh")
        with open(cache_run_sh, "w") as f:
            f.write(run_sh)

        if app_name not in apps:
            apps[app_name] = {}
        apps[app_name][f"v{version}"] = {
            "manifest": manifest,
            "appdir": None,
            "run.sh": cache_run_sh,
            "container_image": image_tag,
        }

    return apps


def _set_docker_root_gcloud():
    from playmolecule.apps import _manifest_to_func, _link_latest_version
    from natsort import natsorted

    app_manifests = _get_apps()

    for appname in app_manifests:
        func_names = _manifest_to_func(appname, app_manifests[appname])
        _link_latest_version(
            appname, natsorted(app_manifests[appname].keys())[-1], func_names
        )


def _get_docker_app_files(manifest):
    from playmolecule._appfiles import _File

    files = {}
    for name, fullpath in manifest["files"].items():
        files[name] = _File(name, fullpath)

    return files


if __name__ == "__main__":
    PROJECT = "repositories-368911"
    REGION = "europe-southwest1"

    results = update_docker_apps_from_gcloud(PROJECT, REGION)
    print("\nSuccessfully pulled and tagged:")
    for c in results:
        print(f" - {c}")

    results = _get_apps(prefix="pm-")
    print("\n" + "=" * 30)
    print("EXTRACTED MANIFESTS")
    print("=" * 30)
    print(json.dumps(results, indent=2))

    # docker run --add-host=host.docker.internal:host-gateway -e ACELLERA_LICENCE_SERVER=27000@host.docker.internal pm-proteinprepare:latest
