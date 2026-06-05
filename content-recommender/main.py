"""Entry point for the content recommender dashboard demo."""

from src.visualizer import Visualizer


def main() -> None:
    visualizer = Visualizer()
    dashboard_path = visualizer.render_dashboard()
    print(f"Dashboard generated at {dashboard_path}")


if __name__ == "__main__":
    main()
