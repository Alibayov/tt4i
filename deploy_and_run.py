import os
import time
import subprocess
import json

DEFAULT_YAML_FILES = {
    "chrome-node": "chrome-node.yaml",
    "chrome-node-hpa": "chrome-node-hpa.yaml",
    "test-controller": "test-controller.yaml"
}

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def check_eks_cluster():
    print("\nChecking available EKS clusters...")
    clusters = run_command(["aws", "eks", "list-clusters", "--output", "json"])
    clusters_json = json.loads(clusters)
    
    if not clusters_json["clusters"]:
        print("No EKS clusters found. Exiting.")
        exit(1)
    
    cluster_list = clusters_json["clusters"]
    
    print("\nAvailable clusters:")
    for i, cluster in enumerate(cluster_list, start=1):
        print(f"{i}) {cluster}")
    
    while True:
        try:
            selection = int(input("\nSelect the cluster number to use: ").strip())
            if 1 <= selection <= len(cluster_list):
                selected_cluster = cluster_list[selection - 1]
                print(f"Using cluster: {selected_cluster}")
                return selected_cluster
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def configure_kubeconfig(cluster):
    print("\nSetting up kubeconfig for the cluster...")
    run_command(["aws", "eks", "update-kubeconfig", "--name", cluster])
    print("Kubeconfig updated.")

def get_yaml_files():
    print("\nBy default, the following YAML files will be used:")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_paths = {key: os.path.join(script_dir, value) for key, value in DEFAULT_YAML_FILES.items()}

    for key, path in default_paths.items():
        print(f" - {key}: {path}")

    use_default = input("\nDo you want to use these default YAML files? (yes/no): ").strip().lower()

    if use_default == "yes":
        return list(default_paths.values())
    else:
        yaml_files = {}
        for key, default_path in default_paths.items():
            custom_path = input(f"Enter path for {key} YAML file (or press Enter to use default: {default_path}): ").strip()
            yaml_files[key] = custom_path if custom_path else default_path

        return list(yaml_files.values())

def apply_kubernetes_resources(yaml_files):
    print("\nDeploying Kubernetes resources...")

    deployment_order = [
        "chrome-node.yaml",
        "chrome-node-hpa.yaml",
        "test-controller.yaml"
    ]
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_map = {os.path.basename(path): path for path in yaml_files}

    for file in deployment_order:
        if file in file_map:
            print(f"Applying {file_map[file]}...")
            run_command(["kubectl", "apply", "-f", file_map[file]])
            print(f"Applied: {file_map[file]}")

            if file == "chrome-node-hpa.yaml":
                print("Waiting 10 seconds before deploying test-controller...")
                time.sleep(10)

def wait_for_pods_ready(label_selector, timeout=120):
    print(f"\nWaiting for pods with label {label_selector} to become ready...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = run_command(["kubectl", "get", "pods", "-l", label_selector, "-o", "json"])
        pods = json.loads(result)
        
        all_ready = all(
            any(cond["type"] == "Ready" and cond["status"] == "True" for cond in pod["status"].get("conditions", []))
            for pod in pods.get("items", [])
        )
        
        if all_ready:
            print(f"All {label_selector} pods are ready!")
            return True
        
        print("Pods are not ready yet. Retrying in 5 seconds...")
        time.sleep(5)
    
    print(f"Timeout reached. {label_selector} pods are still not ready.")
    return False

if __name__ == "__main__":
    selected_cluster = check_eks_cluster()
    configure_kubeconfig(selected_cluster)
    
    yaml_files = get_yaml_files()
    apply_kubernetes_resources(yaml_files)

    if wait_for_pods_ready("app=test-controller") and wait_for_pods_ready("app=chrome-node"):
        print("All required pods are ready! Test-controller will handle test execution.")
    else:
        print("Pods did not become ready. Exiting.")
