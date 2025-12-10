import os
import csv
import random
from typing import Dict, Any, List


OUTPUT_DIR = "dataset"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "code_dataset.csv")


def base_samples() -> List[Dict[str, Any]]:
    """Return a small set of hand-crafted code patterns with typical metrics.

    These act as anchors; the generator will create noisy variations from them.
    """
    return [
        {  # Python, inefficient loop
            "code": """def inefficient_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total
""",
            "language": "python",
            "green_score": 40,
            "energy_wh": 0.06,
            "co2_g": 15.0,
            "cpu_time_ms": 3.0,
            "memory_mb": 10.0,
            "complexity": 4,
            # Environment / runtime-style fields (aligned with Dataset.csv)
            "duration": 0.5,  # seconds
            "emissions": 1.5e-5,
            "emissions_rate": 3.0e-7,
            "energy_consumed": 0.010,  # kWh-style aggregate
            "country_name": "USA",
            "region": "North America",
            "cloud_provider": "AWS",
            "cloud_region": "us-east-1",
            "os": "Windows-11",
            "cpu_model": "Intel i7",
            "gpu_model": "NVIDIA T4",
            "ram_total_size": 16.0,  # GB
            "tracking_mode": "process",
            "on_cloud": "Y",
            "pue": 1.6,
        },
        {  # Python, efficient sum
            "code": """def efficient_sum(numbers):
    return sum(numbers)
""",
            "language": "python",
            "green_score": 85,
            "energy_wh": 0.02,
            "co2_g": 5.0,
            "cpu_time_ms": 0.8,
            "memory_mb": 3.0,
            "complexity": 1,
            "duration": 0.2,
            "emissions": 5.0e-6,
            "emissions_rate": 1.0e-7,
            "energy_consumed": 0.004,
            "country_name": "USA",
            "region": "North America",
            "cloud_provider": "AWS",
            "cloud_region": "us-east-1",
            "os": "Linux",
            "cpu_model": "Intel i7",
            "gpu_model": "NVIDIA T4",
            "ram_total_size": 16.0,
            "tracking_mode": "process",
            "on_cloud": "Y",
            "pue": 1.4,
        },
        {  # JavaScript, inefficient loop
            "code": """function processList(items) {
  const result = [];
  for (let i = 0; i < items.length; i++) {
    if (items[i] > 0) {
      result.push(items[i] * 2);
    }
  }
  return result;
}
""",
            "language": "javascript",
            "green_score": 45,
            "energy_wh": 0.055,
            "co2_g": 13.0,
            "cpu_time_ms": 2.5,
            "memory_mb": 9.0,
            "complexity": 4,
            "duration": 0.4,
            "emissions": 1.3e-5,
            "emissions_rate": 2.8e-7,
            "energy_consumed": 0.009,
            "country_name": "Germany",
            "region": "Europe",
            "cloud_provider": "Azure",
            "cloud_region": "eu-central-1",
            "os": "Linux",
            "cpu_model": "AMD Ryzen 9",
            "gpu_model": "NVIDIA T4",
            "ram_total_size": 32.0,
            "tracking_mode": "machine",
            "on_cloud": "Y",
            "pue": 1.7,
        },
        {  # JavaScript, efficient functional style
            "code": """function processList(items) {
  return items.filter(x => x > 0).map(x => x * 2);
}
""",
            "language": "javascript",
            "green_score": 88,
            "energy_wh": 0.018,
            "co2_g": 4.5,
            "cpu_time_ms": 0.7,
            "memory_mb": 2.8,
            "complexity": 2,
            "duration": 0.15,
            "emissions": 4.0e-6,
            "emissions_rate": 9.0e-8,
            "energy_consumed": 0.003,
            "country_name": "Germany",
            "region": "Europe",
            "cloud_provider": "Azure",
            "cloud_region": "eu-central-1",
            "os": "Linux",
            "cpu_model": "AMD Ryzen 9",
            "gpu_model": "NVIDIA T4",
            "ram_total_size": 32.0,
            "tracking_mode": "machine",
            "on_cloud": "Y",
            "pue": 1.6,
        },
        {  # Java, inefficient indexed loop
            "code": """public List<Integer> inefficientProcess(List<Integer> items) {
    List<Integer> result = new ArrayList<>();
    for (int i = 0; i < items.size(); i++) {
        if (items.get(i) > 0) {
            result.add(items.get(i) * 2);
        }
    }
    return result;
}
""",
            "language": "java",
            "green_score": 42,
            "energy_wh": 0.058,
            "co2_g": 14.0,
            "cpu_time_ms": 2.7,
            "memory_mb": 9.5,
            "complexity": 4,
            "duration": 0.45,
            "emissions": 1.4e-5,
            "emissions_rate": 3.0e-7,
            "energy_consumed": 0.0105,
            "country_name": "India",
            "region": "Asia",
            "cloud_provider": "GCP",
            "cloud_region": "asia-south1",
            "os": "Linux",
            "cpu_model": "Intel Xeon",
            "gpu_model": "NVIDIA A100",
            "ram_total_size": 64.0,
            "tracking_mode": "process",
            "on_cloud": "Y",
            "pue": 1.8,
        },
        {  # Java, efficient streams
            "code": """public List<Integer> efficientProcess(List<Integer> items) {
    return items.stream()
        .filter(x -> x > 0)
        .map(x -> x * 2)
        .collect(Collectors.toList());
}
""",
            "language": "java",
            "green_score": 86,
            "energy_wh": 0.021,
            "co2_g": 5.2,
            "cpu_time_ms": 0.9,
            "memory_mb": 3.2,
            "complexity": 2,
            "duration": 0.18,
            "emissions": 5.0e-6,
            "emissions_rate": 1.1e-7,
            "energy_consumed": 0.0038,
            "country_name": "India",
            "region": "Asia",
            "cloud_provider": "GCP",
            "cloud_region": "asia-south1",
            "os": "Linux",
            "cpu_model": "Intel Xeon",
            "gpu_model": "NVIDIA A100",
            "ram_total_size": 64.0,
            "tracking_mode": "process",
            "on_cloud": "Y",
            "pue": 1.7,
        },
        {  # C++, inefficient process
            "code": """std::vector<int> inefficientProcess(const std::vector<int>& items) {
    std::vector<int> result;
    for (size_t i = 0; i < items.size(); ++i) {
        if (items[i] > 0) {
            result.push_back(items[i] * 2);
        }
    }
    return result;
}
""",
            "language": "cpp",
            "green_score": 48,
            "energy_wh": 0.05,
            "co2_g": 12.0,
            "cpu_time_ms": 2.2,
            "memory_mb": 8.0,
            "complexity": 3,
            "duration": 0.35,
            "emissions": 1.2e-5,
            "emissions_rate": 2.5e-7,
            "energy_consumed": 0.0092,
            "country_name": "France",
            "region": "Europe",
            "cloud_provider": "AWS",
            "cloud_region": "eu-west-3",
            "os": "Linux",
            "cpu_model": "Intel Xeon",
            "gpu_model": "NVIDIA T4",
            "ram_total_size": 32.0,
            "tracking_mode": "machine",
            "on_cloud": "N",
            "pue": 1.5,
        },
        {  # C++, efficient range-based loop
            "code": """std::vector<int> efficientProcess(const std::vector<int>& items) {
    std::vector<int> result;
    result.reserve(items.size());
    for (auto x : items) {
        if (x > 0) {
            result.push_back(x * 2);
        }
    }
    return result;
}
""",
            "language": "cpp",
            "green_score": 82,
            "energy_wh": 0.023,
            "co2_g": 5.8,
            "cpu_time_ms": 1.1,
            "memory_mb": 3.5,
            "complexity": 2,
            "duration": 0.16,
            "emissions": 4.8e-6,
            "emissions_rate": 9.5e-8,
            "energy_consumed": 0.0032,
            "country_name": "France",
            "region": "Europe",
            "cloud_provider": "AWS",
            "cloud_region": "eu-west-3",
            "os": "Linux",
            "cpu_model": "Intel Xeon",
            "gpu_model": "NVIDIA T4",
            "ram_total_size": 32.0,
            "tracking_mode": "machine",
            "on_cloud": "N",
            "pue": 1.4,
        },
    ]


def jitter(value: float, rel: float = 0.15) -> float:
    """Add relative noise to a numeric value."""
    delta = value * rel
    return max(0.0, value + random.uniform(-delta, delta))


def generate_rows(n_rows: int = 6000) -> List[Dict[str, Any]]:
    """Generate a list of synthetic training rows >= n_rows."""
    rows: List[Dict[str, Any]] = []
    bases = base_samples()

    # Ensure at least one copy of each base sample
    for b in bases:
        rows.append(
            dict(
                id=len(rows) + 1,
                code=b["code"],
                language=b["language"],
                green_score=b["green_score"],
                energy_wh=b["energy_wh"],
                co2_g=b["co2_g"],
                cpu_time_ms=b["cpu_time_ms"],
                memory_mb=b["memory_mb"],
                complexity=b["complexity"],
                duration=b["duration"],
                emissions=b["emissions"],
                emissions_rate=b["emissions_rate"],
                energy_consumed=b["energy_consumed"],
                country_name=b["country_name"],
                region=b["region"],
                cloud_provider=b["cloud_provider"],
                cloud_region=b["cloud_region"],
                os=b["os"],
                cpu_model=b["cpu_model"],
                gpu_model=b["gpu_model"],
                ram_total_size=b["ram_total_size"],
                tracking_mode=b["tracking_mode"],
                on_cloud=b["on_cloud"],
                pue=b["pue"],
            )
        )

    # Generate noisy variations
    while len(rows) < n_rows:
        base = random.choice(bases)

        noise_level = random.choice([0.05, 0.1, 0.15, 0.2])

        green = jitter(base["green_score"], noise_level)
        energy = jitter(base["energy_wh"], noise_level)
        co2 = jitter(base["co2_g"], noise_level)
        cpu = jitter(base["cpu_time_ms"], noise_level)
        mem = jitter(base["memory_mb"], noise_level)
        duration = jitter(base["duration"], noise_level)
        emissions = jitter(base["emissions"], noise_level)
        emissions_rate = jitter(base["emissions_rate"], noise_level)
        energy_consumed = jitter(base["energy_consumed"], noise_level)
        comp = max(1, min(10, int(round(jitter(float(base["complexity"]), 0.2)))))

        rows.append(
            dict(
                id=len(rows) + 1,
                code=base["code"],
                language=base["language"],
                green_score=round(max(0.0, min(100.0, green)), 2),
                energy_wh=round(max(0.0001, energy), 6),
                co2_g=round(max(0.0001, co2), 6),
                cpu_time_ms=round(max(0.01, cpu), 4),
                memory_mb=round(max(0.1, mem), 3),
                complexity=comp,
                duration=round(max(0.001, duration), 4),
                emissions=round(max(1e-8, emissions), 8),
                emissions_rate=round(max(1e-9, emissions_rate), 9),
                energy_consumed=round(max(0.000001, energy_consumed), 8),
                country_name=base["country_name"],
                region=base["region"],
                cloud_provider=base["cloud_provider"],
                cloud_region=base["cloud_region"],
                os=base["os"],
                cpu_model=base["cpu_model"],
                gpu_model=base["gpu_model"],
                ram_total_size=base["ram_total_size"],
                tracking_mode=base["tracking_mode"],
                on_cloud=base["on_cloud"],
                pue=round(max(1.0, jitter(base["pue"], 0.05)), 3),
            )
        )

    return rows


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = generate_rows(6000)

    fieldnames = [
        "id",
        "code",
        "language",
        "green_score",
        "energy_wh",
        "co2_g",
        "cpu_time_ms",
        "memory_mb",
        "complexity",
        # Extra columns inspired by Dataset.csv
        "duration",
        "emissions",
        "emissions_rate",
        "energy_consumed",
        "country_name",
        "region",
        "cloud_provider",
        "cloud_region",
        "os",
        "cpu_model",
        "gpu_model",
        "ram_total_size",
        "tracking_mode",
        "on_cloud",
        "pue",
    ]

    with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


