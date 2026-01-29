"""VM management commands: list, delete."""

import json as json_module
import os

import click

from ..config import AgentConfig
from ..http import K8sVMgrAPI, APIError


def _default_api_url():
    return os.environ.get("K8SVMGR_API_URL", "").strip()


def _normalize_api_url(api_url: str) -> str:
    api_url = (api_url or "").strip().rstrip("/")
    if api_url.lower().endswith("/api"):
        api_url = api_url[:-4]
    return api_url


def _extract_data(resp: dict) -> dict:
    return resp.get("data") if isinstance(resp.get("data"), dict) else {}


def _get_authenticated_api(api_url: str = ""):
    """Get authenticated API client or raise error."""
    cfg = AgentConfig.load()
    api_url = _normalize_api_url(api_url or cfg.api_url or _default_api_url())
    if not api_url or not cfg.access_token:
        raise click.ClickException("Not logged in. Run: k8s-agent login")
    return K8sVMgrAPI(api_url, access_token=cfg.access_token), api_url


@click.group()
def vm_commands():
    """VM management commands."""
    pass


@vm_commands.command(name="list")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
@click.option("--format", "output_format", type=click.Choice(["table", "json", "simple"]), default="table", help="Output format")
def list_vms(api_url: str, output_format: str):
    """List all VMs (requires login)."""
    api, _ = _get_authenticated_api(api_url)

    try:
        resp = api.request("GET", "/api/vm")
    except APIError as e:
        raise click.ClickException(str(e))

    data = _extract_data(resp)
    vms = data.get("vms", [])

    if not vms:
        click.echo("No VMs found.")
        return

    if output_format == "json":
        click.echo(json_module.dumps(vms, indent=2, ensure_ascii=False))
    elif output_format == "simple":
        for vm in vms:
            click.echo(f"{vm.get('id', 'N/A')}\t{vm.get('status', 'N/A')}\t{vm.get('machine_type', 'N/A')}")
    else:  # table format
        _print_vm_table(vms)


def _print_vm_table(vms):
    """Print VMs in a condensed table format."""
    from datetime import datetime

    col_widths = {
        "id": 18,
        "status": 12,
        "gpu_model": 14,
        "gpu_num": 5,
        "cpu_num": 5,
        "duration": 12,
        "ip": 16,
        "port": 8,
        "credit": 10,
    }

    # Header: ID, Status, GPU Model, GPU, CPU, Duration, IP, Port, Credit
    header = (
        f"{'ID':<{col_widths['id']}} "
        f"{'Status':<{col_widths['status']}} "
        f"{'GPU Model':<{col_widths['gpu_model']}} "
        f"{'GPU':<{col_widths['gpu_num']}} "
        f"{'CPU':<{col_widths['cpu_num']}} "
        f"{'Duration':<{col_widths['duration']}} "
        f"{'IP Address':<{col_widths['ip']}} "
        f"{'Port':<{col_widths['port']}} "
        f"{'Credit':<{col_widths['credit']}}"
    )
    click.echo(header)
    click.echo("-" * sum(col_widths.values()) + "-" * (len(col_widths) - 1))

    # Rows
    for vm in vms:
        # ID
        vm_id = (vm.get("id") or "N/A")[:col_widths["id"]]

        # Status (second column)
        status = (vm.get("status") or "N/A")[:col_widths["status"]]

        # GPU Model
        gpu_model = (vm.get("gpu_model") or "-")[:col_widths["gpu_model"]]

        # GPU Number
        gpu_num = str(vm.get("gpu_num", 0))[:col_widths["gpu_num"]]

        # CPU Number
        cpu_num = str(vm.get("cpu_num", 0))[:col_widths["cpu_num"]]

        # Duration (calculate from create_time to now)
        create_ts = vm.get("create_time")
        if create_ts:
            duration_sec = int(datetime.now().timestamp() - create_ts)
            # Handle negative durations (e.g., clock skew or future timestamps)
            if duration_sec < 0:
                duration = "0h 0m"
            else:
                hours = duration_sec // 3600
                minutes = (duration_sec % 3600) // 60
                duration = f"{hours}h {minutes}m"
        else:
            duration = "-"
        duration = duration[:col_widths["duration"]]

        # Host IP
        host_ip = (vm.get("host_ip") or "-")[:col_widths["ip"]]

        # Port
        svc_port = (vm.get("svc_port") or "-")[:col_widths["port"]]

        # Used credit
        used_credit = vm.get("used_credit")
        credit_str = f"{used_credit:.1f}" if used_credit is not None else "-"
        credit_str = credit_str[:col_widths["credit"]]

        row = (
            f"{vm_id:<{col_widths['id']}} "
            f"{status:<{col_widths['status']}} "
            f"{gpu_model:<{col_widths['gpu_model']}} "
            f"{gpu_num:<{col_widths['gpu_num']}} "
            f"{cpu_num:<{col_widths['cpu_num']}} "
            f"{duration:<{col_widths['duration']}} "
            f"{host_ip:<{col_widths['ip']}} "
            f"{svc_port:<{col_widths['port']}} "
            f"{credit_str:<{col_widths['credit']}}"
        )
        click.echo(row)

    click.echo(f"\nTotal: {len(vms)} VM(s)")


@vm_commands.command(name="create")
@click.option("--vm-id", "vm_id", help="VM ID (auto-generated if not specified)")
@click.option("--cpu", type=int, help="Number of CPUs")
@click.option("--gpu", type=int, default=0, help="Number of GPUs (default: 0)")
@click.option("--gpu-model", "gpu_model", help="GPU model (e.g., A800-80G-R)")
@click.option("--shm", type=int, help="Shared memory in GB")
@click.option("--driver-version", "driver_version", help="GPU driver version (default: 535)")
@click.option("--image", help="Docker image URL")
@click.option("--command", help="Custom command to run")
@click.option("--args", help="Arguments for the command")
@click.option("--key", type=int, help="SSH public key ID")
@click.option("--zero", is_flag=True, help="Mark as zero machine (primary backup machine)")
@click.option("--experimental", is_flag=True, help="Mark as experimental machine")
@click.option("--purpose", help="Purpose/description of the VM")
@click.option("--max-idle-hrs", "max_idle_hrs", type=int, help="Max idle hours before auto-shutdown")
# @click.option("--node-name", "node_name", help="Specific node to schedule on")
# @click.option("--privileged", is_flag=True, help="Run in privileged mode")
# @click.option("--cap-add-sys-admin", "cap_add_sys_admin", is_flag=True, help="Add SYS_ADMIN capability")
@click.option("--check", "-c", is_flag=True, help="Check availability only (don't create VM)")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
def create_vm(vm_id, cpu, gpu, gpu_model, shm, driver_version, image, command, args, key,
              zero, experimental, purpose, max_idle_hrs, check, api_url):
    """Create a new VM (requires login).

    Examples:
        # Check availability for CPU machine
        k8s-agent create --cpu 16 --check

        # Check availability for GPU machine
        k8s-agent create --gpu 2 --gpu-model A800-80G-R --check

        # CPU machine
        k8s-agent create --cpu 16

        # GPU machine
        k8s-agent create --gpu 2 --gpu-model A800-80G-R

        # Full specification
        k8s-agent create --gpu 4 --gpu-model A800-80G-R --shm 32 --image harbor.example.com/ml/pytorch:latest --purpose "Training model"
    """
    api, _ = _get_authenticated_api(api_url)

    try:
        # Validate GPU requirements
        if gpu and gpu > 0:
            if not gpu_model:
                raise click.ClickException("--gpu-model is required when creating GPU machines")

        # Check availability mode
        if check:
            click.echo("Checking availability...")

            # Build query parameters
            params = []
            if cpu:
                params.append(f"cpu={cpu}")
            if gpu and gpu > 0:
                params.append(f"gpu={gpu}")
                params.append(f"gpu_model={gpu_model}")
                if driver_version:
                    params.append(f"driver_version={driver_version}")

            # Build URL with query string
            query_string = "&".join(params)
            endpoint = f"/api/vm/availability?{query_string}" if query_string else "/api/vm/availability"

            # Query availability endpoint
            resp = api.request("GET", endpoint)
            data = resp.get("data", {})

            total = data.get("total", 0)
            available_nodes = data.get("items", [])

            if total > 0:
                click.echo(f"✓ {total} node(s) available")
                if available_nodes:
                    click.echo(f"\nAvailable nodes:")
                    for node in available_nodes:
                        click.echo(f"  - {node}")
            else:
                click.echo("✗ No nodes available for the specified configuration")

            return  # Exit without creating VM

        # Build request body matching frontend formData structure
        limit = {
            "gpu": gpu or 0,
            "storage": 0,
            "local_storage": 200,
        }

        if cpu is not None:
            limit["cpu"] = cpu
        if gpu_model:
            limit["gpu_model"] = gpu_model
        if shm is not None:
            limit["shm"] = shm

        body = {
            "limit": limit,
            "machines": [],
            "zero": zero,
            "preemptive": False,
        }

        # Optional parameters
        if vm_id:
            body["vm_id"] = vm_id
        if key is not None:
            body["public_key"] = key
        if image:
            body["image"] = image
        if command:
            body["command"] = command
        if args:
            body["args"] = args
        if purpose:
            body["purpose"] = purpose
        if driver_version:
            body["driver_version"] = driver_version
        if experimental:
            body["experimental"] = experimental
        if max_idle_hrs is not None:
            body["max_idle_hrs"] = max_idle_hrs

        # Create VM
        click.echo("Creating VM...")
        resp = api.request("POST", "/api/vm", json_body=body)

        data = resp.get("data", {})
        if data.get("pending"):
            click.echo("⚠ VM is pending - waiting for cluster resources.")
        else:
            click.echo("✓ VM creation request submitted successfully.")

        # Show summary
        machine_type_str = f"{gpu_model} x{gpu}" if gpu and gpu > 0 else f"CPU x{cpu or 8}"
        click.echo(f"\nVM Configuration:")
        click.echo(f"  Type: {machine_type_str}")
        if shm:
            click.echo(f"  Shared Memory: {shm}GB")
        if image:
            click.echo(f"  Image: {image}")
        if purpose:
            click.echo(f"  Purpose: {purpose}")

        flags = []
        if zero:
            flags.append("Zero machine")
        if experimental:
            flags.append("Experimental")
        if flags:
            click.echo(f"  Flags: {', '.join(flags)}")

        click.echo("\nUse 'k8s-agent list' to check VM status.")

    except APIError as e:
        error_msg = str(e)
        raise click.ClickException(f"Failed to create VM: {error_msg}")


@vm_commands.command(name="events")
@click.argument("vm_id")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
def vm_events(vm_id: str, api_url: str):
    """Get VM events (requires login).

    Examples:
        k8s-agent events my-vm-001
    """
    api, _ = _get_authenticated_api(api_url)

    try:
        endpoint = f"/api/vm/events?vmid={vm_id}"
        resp = api.request("GET", endpoint)

        data = resp.get("data", {})
        events = data if isinstance(data, list) else data.get("events", [])

        if not events:
            click.echo("No events found for this VM.")
            return

        click.echo(f"Events for VM '{vm_id}':\n")
        for event in events:
            # Handle both dict and object formats
            if isinstance(event, dict):
                event_type = event.get("type", "N/A")
                reason = event.get("reason", "N/A")
                message = event.get("message", "N/A")
                timestamp = event.get("last_timestamp", event.get("timestamp", "N/A"))
            else:
                event_type = getattr(event, "type", "N/A")
                reason = getattr(event, "reason", "N/A")
                message = getattr(event, "message", "N/A")
                timestamp = getattr(event, "last_timestamp", getattr(event, "timestamp", "N/A"))

            click.echo(f"[{timestamp}] {event_type}: {reason}")
            click.echo(f"  {message}\n")

    except APIError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise click.ClickException(f"VM '{vm_id}' not found.")
        raise click.ClickException(f"Failed to get events: {error_msg}")


@vm_commands.command(name="logs")
@click.argument("vm_id")
@click.option("--tail", type=int, help="Number of lines to show from the end")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
def vm_logs(vm_id: str, tail: int, api_url: str):
    """Get VM logs (requires login).

    Examples:
        k8s-agent logs my-vm-001
        k8s-agent logs my-vm-001 --tail 100
    """
    api, _ = _get_authenticated_api(api_url)

    try:
        endpoint = f"/api/vm/logs?vmid={vm_id}"
        if tail:
            endpoint += f"&tail={tail}"

        resp = api.request("GET", endpoint)

        data = resp.get("data", {})
        logs = data if isinstance(data, str) else data.get("logs", "")

        if not logs:
            click.echo("No logs available for this VM.")
            return

        click.echo(logs)

    except APIError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise click.ClickException(f"VM '{vm_id}' not found.")
        raise click.ClickException(f"Failed to get logs: {error_msg}")


@vm_commands.command(name="dashboard")
@click.argument("vm_id")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
def vm_dashboard(vm_id: str, api_url: str):
    """Get VM dashboard metrics with visual charts (requires login).

    Examples:
        k8s-agent dashboard my-vm-001
    """
    api, _ = _get_authenticated_api(api_url)

    try:
        endpoint = f"/api/vm/dashboard?vmid={vm_id}"
        resp = api.request("GET", endpoint)

        data = resp.get("data", {})

        if not data:
            click.echo("No dashboard data available for this VM.")
            return

        click.echo(f"╔═══════════════════════════════════════════════════════════════╗")
        click.echo(f"║  Dashboard: {vm_id:<48}║")
        click.echo(f"╚═══════════════════════════════════════════════════════════════╝\n")

        # Display memory metrics
        memory_metrics = data.get("memory_metrics", {})
        if memory_metrics:
            _display_memory_section(memory_metrics)

        # Display GPU metrics
        gpu_metrics = data.get("gpu_metrics", {})
        if gpu_metrics:
            for gpu_idx, (uuid, metrics) in enumerate(gpu_metrics.items()):
                _display_gpu_section(uuid, metrics, gpu_idx)

    except APIError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise click.ClickException(f"VM '{vm_id}' not found.")
        raise click.ClickException(f"Failed to get dashboard: {error_msg}")


def _display_memory_section(metrics):
    """Display memory metrics with gauge chart."""
    mem_used_list = metrics.get("mem_used", [])
    mem_free_list = metrics.get("mem_free", [])

    if not mem_used_list or not mem_free_list:
        return

    # Get latest values
    mem_used = mem_used_list[-1] if mem_used_list else 0
    mem_free = mem_free_list[-1] if mem_free_list else 0
    mem_total = mem_used + mem_free

    if mem_total == 0:
        return

    mem_percent = (mem_used / mem_total) * 100

    click.echo("┌─────────────────────────────────────────────────────────────┐")
    click.echo("│ 💾 MEMORY                                                    │")
    click.echo("├─────────────────────────────────────────────────────────────┤")

    # Gauge chart
    _print_gauge(mem_percent, f"Memory Usage: {mem_used:.1f}GB / {mem_total:.1f}GB")

    # Simple sparkline for memory usage over time
    if len(mem_used_list) > 1:
        click.echo("│                                                             │")
        mem_percentages = [(u / (u + f) * 100) if (u + f) > 0 else 0
                          for u, f in zip(mem_used_list, mem_free_list)]
        _print_sparkline(mem_percentages, "Memory Trend", "%")

    click.echo("└─────────────────────────────────────────────────────────────┘\n")


def _display_gpu_section(uuid, metrics, gpu_idx):
    """Display GPU metrics with gauges and sparklines."""
    gpu_util_list = metrics.get("gpu_utilization", [])
    mem_util_list = metrics.get("memory_utilization", [])
    gpu_mem_used_list = metrics.get("gpu_memory_used", [])
    gpu_mem_free_list = metrics.get("gpu_memory_free", [])
    power_list = metrics.get("power_usage", [])
    temp_list = metrics.get("gpu_temp", [])

    if not gpu_util_list:
        return

    # Get latest values
    gpu_util = gpu_util_list[-1] if gpu_util_list else 0
    mem_util = mem_util_list[-1] if mem_util_list else 0
    gpu_mem_used = gpu_mem_used_list[-1] if gpu_mem_used_list else 0
    gpu_mem_free = gpu_mem_free_list[-1] if gpu_mem_free_list else 0
    gpu_mem_total = gpu_mem_used + gpu_mem_free
    power = power_list[-1] if power_list else 0
    temp = temp_list[-1] if temp_list else 0

    # Truncate UUID for display
    uuid_short = uuid[:8] + "..." if len(uuid) > 8 else uuid

    click.echo("┌─────────────────────────────────────────────────────────────┐")
    click.echo(f"│ 🎮 GPU #{gpu_idx} ({uuid_short:<45}) │")
    click.echo("├─────────────────────────────────────────────────────────────┤")

    # GPU Utilization Gauge
    _print_gauge(gpu_util, f"GPU Utilization")

    click.echo("│                                                             │")

    # GPU Memory Gauge
    if gpu_mem_total > 0:
        mem_percent = (gpu_mem_used / gpu_mem_total) * 100
        _print_gauge(mem_percent, f"GPU Memory: {gpu_mem_used:.1f}GB / {gpu_mem_total:.1f}GB")
    else:
        _print_gauge(mem_util, f"GPU Memory Utilization")

    click.echo("│                                                             │")

    # Temperature and Power as text
    temp_bar = _get_bar(temp, 100, 20)
    power_bar = _get_bar(power, 400, 20)

    click.echo(f"│  🌡  Temperature: {temp:>5.1f}°C  {temp_bar}                │")
    click.echo(f"│  ⚡ Power Usage: {power:>6.1f}W  {power_bar}                │")

    # Sparklines for trends
    if len(gpu_util_list) > 1:
        click.echo("│                                                             │")
        _print_sparkline(gpu_util_list, "GPU Util Trend", "%")

    if len(power_list) > 1:
        _print_sparkline(power_list, "Power Trend", "W")

    if len(temp_list) > 1:
        _print_sparkline(temp_list, "Temp Trend", "°C")

    click.echo("└─────────────────────────────────────────────────────────────┘\n")


def _print_gauge(percent, label):
    """Print a gauge chart for the given percentage."""
    # Ensure percent is in 0-100 range
    percent = max(0, min(100, percent))

    # Determine color/symbol based on percentage
    if percent >= 90:
        symbol = "█"
        status = "⚠"
    elif percent >= 70:
        symbol = "▓"
        status = "●"
    else:
        symbol = "▒"
        status = "●"

    # Create gauge (40 chars wide)
    gauge_width = 40
    filled = int((percent / 100) * gauge_width)
    gauge = symbol * filled + "░" * (gauge_width - filled)

    click.echo(f"│  {status} {label:<22}                              │")
    click.echo(f"│  [{gauge}] {percent:>5.1f}%  │")


def _get_bar(value, max_value, width=20):
    """Get a simple bar representation."""
    if max_value == 0:
        return "░" * width

    filled = int((value / max_value) * width)
    filled = max(0, min(width, filled))
    return "▓" * filled + "░" * (width - filled)


def _print_sparkline(values, label, unit):
    """Print a simple sparkline chart."""
    if not values or len(values) < 2:
        return

    # Use only recent values (last 30)
    values = values[-30:]

    # Create sparkline using unicode characters
    spark_chars = "▁▂▃▄▅▆▇█"

    if not values:
        return

    min_val = min(values)
    max_val = max(values)

    # Avoid division by zero
    if max_val == min_val:
        sparkline = spark_chars[0] * len(values)
    else:
        sparkline = "".join([
            spark_chars[min(int((v - min_val) / (max_val - min_val) * (len(spark_chars) - 1)), len(spark_chars) - 1)]
            for v in values
        ])

    # Truncate sparkline to fit
    sparkline = sparkline[:45]
    current_val = values[-1]

    click.echo(f"│  {label:<15} {sparkline} {current_val:>6.1f}{unit:<3}  │")


@vm_commands.command(name="interconnect")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
def vm_interconnect(api_url: str):
    """Interconnect all running VMs for the current user (requires login).

    Sets up SSH key-based authentication between all running VMs.

    Examples:
        k8s-agent interconnect
    """
    api, _ = _get_authenticated_api(api_url)

    try:
        click.echo("Setting up VM interconnection...")
        resp = api.request("PUT", "/api/vm/interconnect")

        data = resp.get("data", "")

        click.echo("✓ VMs interconnected successfully.\n")

        if data:
            click.echo("Deepspeed Hostfile:")
            click.echo(data)
            click.echo("\nYou can now SSH between VMs using: ssh <vm-id>")

    except APIError as e:
        error_msg = str(e)
        if "no running vms" in error_msg.lower():
            raise click.ClickException("No running VMs to interconnect.")
        raise click.ClickException(f"Failed to interconnect VMs: {error_msg}")


@vm_commands.command(name="delete")
@click.argument("vm_id")
@click.option("--api-url", "api_url", default="", help="Override API base URL")
@click.option("--force", is_flag=True, default=False, help="Force delete without confirmation")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt")
def delete_vm(vm_id: str, api_url: str, force: bool, yes: bool):
    """Delete a VM by ID (requires login).
    
    Examples:
        k8s-agent delete my-vm-001
        k8s-agent delete my-vm-001 --yes
        k8s-agent delete my-vm-001 --force
    """
    api, _ = _get_authenticated_api(api_url)

    # Confirm deletion
    if not yes and not force:
        if not click.confirm(f"Are you sure you want to delete VM '{vm_id}'?"):
            click.echo("Cancelled.")
            return

    # Delete VM
    try:
        if force:
            # Force delete endpoint expects {"id": vm_id}
            endpoint = "/api/vm/force"
            json_body = {"id": vm_id}
        else:
            # Normal delete endpoint expects {"ids": [vm_id]}
            endpoint = "/api/vm"
            json_body = {"ids": [vm_id]}

        resp = api.request("DELETE", endpoint, json_body=json_body)
        click.echo(f"✓ VM '{vm_id}' deletion initiated successfully.")

        if force:
            click.echo("  (Force deleted - VM removed immediately)")
        else:
            click.echo("  (VM will be deleted)")
    except APIError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise click.ClickException(f"VM '{vm_id}' not found. Use 'k8s-agent list' to see available VMs.")
        raise click.ClickException(f"Failed to delete VM: {error_msg}")
