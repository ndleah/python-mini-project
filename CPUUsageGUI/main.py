import psutil
import matplotlib.pyplot as plt


def plot_system_metrics():
    # Get CPU cores usage
    cpu_usage = psutil.cpu_percent(percpu=True)

    # Get Memory usage
    mem = psutil.virtual_memory()

    # Get the number of running containers (this is just a placeholder)
    num_running_containers = 5  # Replace this with actual logic to get container count

    # Plot CPU cores usage
    plt.subplot(3, 1, 1)
    plt.plot(cpu_usage, marker="o")
    plt.title("CPU Cores Usage")
    plt.xlabel("CPU Core")
    plt.ylabel("Usage (%)")

    # Plot Memory usage
    plt.subplot(3, 1, 2)
    plt.bar(["Used", "Available", "Free"], [mem.used, mem.available, mem.free])
    plt.title("Memory Usage")
    plt.ylabel("Bytes")

    # Plot Number of running containers
    plt.subplot(3, 1, 3)
    plt.bar(["Running Containers"], [num_running_containers])
    plt.title("Number of Running Containers")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_system_metrics()
