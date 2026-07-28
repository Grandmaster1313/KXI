from pathlib import Path


def write_dashboard(html):

    dashboard = (
        Path(__file__).resolve().parent
        / "dashboard"
        / "index.html"
    )

    dashboard.parent.mkdir(exist_ok=True)

    with open(
        dashboard,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print(f"Dashboard updated successfully.")
    print(f"Saved to: {dashboard}")