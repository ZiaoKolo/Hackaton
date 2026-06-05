"""Dashboard rendering helpers for the content recommender demo."""

from __future__ import annotations

from pathlib import Path
import webbrowser

import matplotlib.pyplot as plt
import seaborn as sns


DEMO_USERS = [
        {"id": 1, "name": "Alice", "age": 22, "interests": ["Technology", "Music"], "score": 3.0},
        {"id": 2, "name": "Bob", "age": 35, "interests": ["Fitness", "Books"], "score": 4.0},
        {"id": 3, "name": "Claire", "age": 58, "interests": ["Fitness"], "score": 1.0},
        {"id": 4, "name": "David", "age": 19, "interests": ["Music"], "score": 2.0},
        {"id": 5, "name": "Emma", "age": 45, "interests": ["Technology", "Books", "Fitness"], "score": 6.0},
]

DEMO_RECOMMENDATIONS = {
        1: [
                {"id": 101, "title": "AI Music Generator", "category": "Technology", "relevance": 94},
                {"id": 102, "title": "Synthwave Beats", "category": "Music", "relevance": 88},
        ],
        2: [
                {"id": 201, "title": "Marathon Guide", "category": "Fitness", "relevance": 92},
                {"id": 202, "title": "Nutrition Science", "category": "Books", "relevance": 85},
        ],
        3: [{"id": 301, "title": "Yoga for Seniors", "category": "Fitness", "relevance": 97}],
        4: [{"id": 401, "title": "Guitar Tabs Pro", "category": "Music", "relevance": 89}],
        5: [
                {"id": 501, "title": "Tech Startup Memoir", "category": "Books", "relevance": 95},
                {"id": 502, "title": "Wearable Tech Review", "category": "Technology", "relevance": 91},
                {"id": 503, "title": "HIIT Workouts", "category": "Fitness", "relevance": 84},
        ],
}

DEMO_INSIGHTS = [
        "Fitness performs 32% above average in morning segments.",
        "Technology and Music users exhibit a 0.8 correlation overlap.",
        "Emma has recommendation confidence above 90% for Tech.",
        "Books show highest long-term retention globally.",
]

HEATMAP_VALUES = [
        12, 45, 80, 20, 10, 5, 90, 100,
        30, 40, 50, 60, 70, 80, 90, 10,
        25, 35, 45, 55, 65, 75, 85, 95,
        100, 80, 60, 40, 20, 10, 5, 0,
]

SIMILARITY = [
        [1.0, 0.2, 0.1, 0.8, 0.6],
        [0.2, 1.0, 0.5, 0.1, 0.7],
        [0.1, 0.5, 1.0, 0.0, 0.4],
        [0.8, 0.1, 0.0, 1.0, 0.3],
        [0.6, 0.7, 0.4, 0.3, 1.0],
]


class Visualizer:
        def __init__(self, output_dir: str | Path = "outputs") -> None:
                self.output_dir = Path(output_dir)
                self.output_dir.mkdir(parents=True, exist_ok=True)

        def _clean_outputs(self) -> None:
                for path in self.output_dir.glob("*"):
                        if path.is_file():
                                path.unlink()

        def _plot_base_style(self, theme: str = "dark") -> None:
                is_dark = theme == "dark"
                background = "#111827" if is_dark else "#F8FAFC"
                text = "#F8FAFC" if is_dark else "#0F172A"
                muted = "#94A3B8" if is_dark else "#64748B"
                grid = "#334155" if is_dark else "#CBD5E1"

                sns.set_theme(
                        style="whitegrid",
                        context="notebook",
                        rc={
                                "axes.facecolor": background,
                                "figure.facecolor": background,
                                "axes.edgecolor": grid,
                                "axes.labelcolor": text,
                                "xtick.color": muted,
                                "ytick.color": muted,
                                "text.color": text,
                                "grid.color": grid,
                                "grid.linestyle": "-",
                                "grid.alpha": 0.35 if is_dark else 0.55,
                                "axes.titleweight": "bold",
                                "font.family": ["DejaVu Sans", "Arial", "sans-serif"],
                                # Agrandir toutes les fontes globalement
                                "font.size": 18,
                                "axes.titlesize": 26,
                                "axes.labelsize": 20,
                                "xtick.labelsize": 18,
                                "ytick.labelsize": 18,
                        },
                )

        def _finish_figure(self, output_name: str, theme: str = "dark") -> Path:
                output_path = self.output_dir / output_name
                facecolor = "#111827" if theme == "dark" else "#F8FAFC"
                # pad_inches réduit pour que le graphique remplisse mieux
                plt.savefig(
                        output_path,
                        dpi=220,
                        bbox_inches="tight",
                        pad_inches=0.25,
                        facecolor=facecolor,
                        edgecolor="none",
                )
                plt.close()
                return output_path

        def plot_categories(self, theme: str = "dark") -> Path:
                categories = ["Book", "Playlist", "Fitness"]
                counts = [10, 7, 5]

                self._plot_base_style(theme)

                # Grande figure — sera affichée plein-card
                fig, ax = plt.subplots(figsize=(18, 10))

                colors = ["#7C6FF7", "#F59E0B", "#10B981"]
                edge = "#0F172A" if theme == "dark" else "#FFFFFF"
                label_color = "#F8FAFC" if theme == "dark" else "#0F172A"

                bars = ax.bar(
                        categories,
                        counts,
                        color=colors,
                        width=0.60,
                        edgecolor=edge,
                        linewidth=1.8,
                )

                ax.set_title("Contenus par catégorie", pad=30)
                ax.set_ylabel("Volume", fontweight="bold")
                ax.set_xlabel("")

                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_color("#334155" if theme == "dark" else "#CBD5E1")
                ax.spines["bottom"].set_color("#334155" if theme == "dark" else "#CBD5E1")
                ax.set_axisbelow(True)

                ax.bar_label(
                        bars,
                        padding=10,
                        color=label_color,
                        fontsize=22,
                        fontweight="bold",
                )

                ax.set_ylim(0, max(counts) + 5)
                plt.tight_layout(pad=1.5)

                return self._finish_figure(f"categories-{theme}.png", theme)

        def plot_tags(self, theme: str = "dark") -> Path:
                tags = ["technology", "music", "ai", "fitness"]
                counts = [8, 6, 5, 3]

                self._plot_base_style(theme)
                fig, ax = plt.subplots(figsize=(18, 10))

                palette = ["#06B6D4", "#F59E0B", "#7C6FF7", "#10B981"]
                edge = "#0F172A" if theme == "dark" else "#FFFFFF"
                label_color = "#F8FAFC" if theme == "dark" else "#0F172A"

                bars = ax.barh(tags, counts, color=palette, height=0.58, edgecolor=edge, linewidth=1.4)

                ax.set_title("Distribution des tags", pad=30)
                ax.set_xlabel("Occurrences", fontweight="bold")
                ax.set_ylabel("")

                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_color("#334155" if theme == "dark" else "#CBD5E1")
                ax.spines["bottom"].set_color("#334155" if theme == "dark" else "#CBD5E1")

                ax.set_xlim(0, max(counts) + 2.5)

                for bar, value in zip(bars, counts):
                        ax.text(
                                value + 0.18,
                                bar.get_y() + bar.get_height() / 2,
                                str(value),
                                va="center",
                                ha="left",
                                color=label_color,
                                fontsize=20,
                                fontweight="bold",
                        )

                plt.tight_layout(pad=1.5)
                return self._finish_figure(f"tags-{theme}.png", theme)

        def plot_scores(self, theme: str = "dark") -> Path:
                scores = [0.9, 0.7, 0.5, 0.3]

                self._plot_base_style(theme)
                fig, ax = plt.subplots(figsize=(18, 10))

                x_values = list(range(1, len(scores) + 1))
                ax.plot(
                        x_values,
                        scores,
                        color="#7C6FF7",
                        linewidth=4.0,
                        marker="o",
                        markersize=14,
                        markerfacecolor="#7C6FF7",
                        markeredgewidth=2.5,
                        markeredgecolor="#F8FAFC" if theme == "dark" else "#0F172A",
                )
                ax.fill_between(x_values, scores, color="#7C6FF7", alpha=0.20)

                ax.set_title("Scores de recommandation", pad=30)
                ax.set_xlabel("Segments", fontweight="bold")
                ax.set_ylabel("Score", fontweight="bold")
                ax.set_ylim(0, 1.05)
                ax.set_xticks(x_values)
                ax.set_xticklabels(["S1", "S2", "S3", "S4"])

                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_color("#334155" if theme == "dark" else "#CBD5E1")
                ax.spines["bottom"].set_color("#334155" if theme == "dark" else "#CBD5E1")
                ax.margins(x=0.06)

                plt.tight_layout(pad=1.5)
                return self._finish_figure(f"scores-{theme}.png", theme)

        def render_dashboard(self, selected_user_id: int = 5) -> Path:
                self._clean_outputs()

                categories_dark_path = self.plot_categories("dark").name
                categories_light_path = self.plot_categories("light").name
                tags_dark_path = self.plot_tags("dark").name
                tags_light_path = self.plot_tags("light").name
                scores_dark_path = self.plot_scores("dark").name
                scores_light_path = self.plot_scores("light").name

                html = self._build_dashboard_html(
                        selected_user_id,
                        categories_dark_path,
                        categories_light_path,
                        tags_dark_path,
                        tags_light_path,
                        scores_dark_path,
                        scores_light_path,
                )
                dashboard_path = self.output_dir / "dashboard.html"
                dashboard_path.write_text(html, encoding="utf-8")
                return dashboard_path

        def open_dashboard(self, selected_user_id: int = 5) -> Path:
                dashboard_path = self.render_dashboard(selected_user_id=selected_user_id)
                webbrowser.open(dashboard_path.as_uri())
                return dashboard_path

        def _build_dashboard_html(
                self,
                selected_user_id: int,
                categories_dark_path: str,
                categories_light_path: str,
                tags_dark_path: str,
                tags_light_path: str,
                scores_dark_path: str,
                scores_light_path: str,
        ) -> str:
                users_markup = []
                for user in DEMO_USERS:
                        active = user["id"] == selected_user_id
                        interests = "".join(
                                f'<span class="chip chip-{interest.lower()}">{interest}</span>'
                                for interest in user["interests"]
                        )
                        users_markup.append(
                                f"""
                                <tr class="{'active-row' if active else ''}">
                                    <td>{user['name']}</td>
                                    <td class="mono muted">{user['age']}</td>
                                    <td><div class="chips">{interests}</div></td>
                                    <td class="mono muted">{user['score']:.1f}</td>
                                    <td class="text-right"><button class="{'btn-primary' if active else 'btn-secondary'}">Recommend</button></td>
                                </tr>
                                """
                        )

                recommendation_markup = []
                for item in DEMO_RECOMMENDATIONS.get(selected_user_id, []):
                        recommendation_markup.append(
                                f"""
                                <div class="reco-card">
                                    <div class="reco-head">
                                        <div>
                                            <h3>{item['title']}</h3>
                                            <span class="chip chip-{item['category'].lower()}">{item['category']}</span>
                                        </div>
                                        <span class="mono success">{item['relevance']}% Match</span>
                                    </div>
                                    <div class="progress"><div style="width: {item['relevance']}%;"></div></div>
                                    <div class="tags-row"><span>#personalized</span><span>#ml-generated</span></div>
                                </div>
                                """
                        )

                heatmap_markup = []
                for value in HEATMAP_VALUES:
                        heatmap_markup.append(
                                f'<div class="heat-cell" title="Activity: {value}%" style="background: rgba(6, 182, 212, {max(0.1, value / 100):.2f});"></div>'
                        )

                similarity_markup = []
                names = ["Alice", "Bob", "Claire", "David", "Emma"]
                for row_index, row in enumerate(SIMILARITY):
                        for col_index, value in enumerate(row):
                                similarity_markup.append(
                                        f'<div class="sim-cell" title="{names[row_index]} x {names[col_index]}: {value:.2f}" style="background: rgba(124, 111, 247, {value});"></div>'
                                )

                insights_markup = "".join(
                        f"""
                        <div class="insight-card">
                            <div class="dot"></div>
                            <p>{insight}</p>
                        </div>
                        """
                        for insight in DEMO_INSIGHTS
                )

                target_name = next(user["name"] for user in DEMO_USERS if user["id"] == selected_user_id)

                return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ContentAI Analytics</title>
    <style>
        :root {{
            --bg: #0B1020;
            --sidebar: #0D1424;
            --card: rgba(17, 24, 39, 0.94);
            --border: rgba(255,255,255,0.07);
            --text: #F8FAFC;
            --muted: #94A3B8;
            --primary: #7C6FF7;
            --success: #10B981;
            --sidebar-w: 240px;
        }}

        *, *::before, *::after {{ box-sizing: border-box; }}

        body {{
            margin: 0;
            min-height: 100vh;
            background: var(--bg);
            color: var(--text);
            font-family: Inter, Arial, sans-serif;
            display: flex;
            overflow: hidden;
            height: 100vh;
        }}

        /* ── SIDEBAR ── */
        .sidebar {{
            width: var(--sidebar-w);
            flex-shrink: 0;
            background: var(--sidebar);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            height: 100vh;
            position: fixed;
            left: 0; top: 0;
            z-index: 20;
            padding: 0 0 24px;
            transition: width 0.25s ease;
        }}

        .sidebar-brand {{
            height: 64px;
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 20px;
            border-bottom: 1px solid var(--border);
            font-weight: 700;
            font-size: 15px;
            letter-spacing: -0.03em;
            flex-shrink: 0;
        }}

        .brand-icon {{
            width: 32px;
            height: 32px;
            border-radius: 10px;
            display: grid;
            place-items: center;
            background: rgba(124,111,247,0.15);
            color: var(--primary);
            font-size: 16px;
            flex-shrink: 0;
        }}

        .nav {{ display: flex; flex-direction: column; gap: 4px; padding: 16px 12px; flex: 1; }}

        .nav-section-label {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.12em;
            color: var(--muted);
            text-transform: uppercase;
            padding: 8px 8px 4px;
            margin-top: 8px;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            color: var(--muted);
            border: none;
            background: transparent;
            width: 100%;
            text-align: left;
            transition: background 0.15s, color 0.15s;
            white-space: nowrap;
        }}

        .nav-item:hover {{ background: rgba(255,255,255,0.05); color: var(--text); }}

        .nav-item.active {{
            background: rgba(124,111,247,0.14);
            color: var(--primary);
            font-weight: 600;
        }}

        .nav-item .nav-icon {{
            width: 20px;
            text-align: center;
            flex-shrink: 0;
            font-size: 16px;
        }}

        .nav-badge {{
            margin-left: auto;
            background: rgba(124,111,247,0.18);
            color: var(--primary);
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 999px;
        }}

        .sidebar-footer {{
            padding: 0 12px;
            flex-shrink: 0;
        }}

        /* ── MAIN AREA ── */
        .main {{
            margin-left: var(--sidebar-w);
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }}

        .topbar {{
            height: 64px;
            border-bottom: 1px solid var(--border);
            background: rgba(11,16,32,0.85);
            backdrop-filter: blur(18px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 28px;
            flex-shrink: 0;
        }}

        .topbar-title {{
            font-size: 18px;
            font-weight: 600;
            letter-spacing: -0.02em;
        }}

        .topbar-right {{ display: flex; align-items: center; gap: 12px; }}

        .button {{
            width: 36px; height: 36px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.04);
            color: var(--muted);
            cursor: pointer;
            font-size: 16px;
            display: grid;
            place-items: center;
        }}

        /* ── SCROLLABLE CONTENT ── */
        .content {{
            flex: 1;
            overflow-y: auto;
            padding: 28px;
            background: radial-gradient(circle at top right, rgba(124,111,247,0.1), transparent 30%),
                        radial-gradient(circle at left bottom, rgba(6,182,212,0.08), transparent 24%),
                        var(--bg);
        }}

        /* ── SECTIONS (tab panels) ── */
        .section {{ display: none; animation: fadeIn 0.22s ease; }}
        .section.active {{ display: block; }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}

        /* ── GRIDS ── */
        .grid {{ display: grid; gap: 24px; }}
        .grid-4 {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
        .grid-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .grid-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
        .spacer {{ height: 24px; }}

        /* ── CARDS ── */
        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 18px 42px rgba(2,6,23,0.18);
            display: flex;
            flex-direction: column;
        }}

        .chart-wrapper {{
            flex: 1;
            display: flex;
            align-items: stretch;
            min-height: 0;
        }}

        .chart-img {{
            width: 100%;
            height: 100%;
            min-height: 420px;
            object-fit: fill;
            display: block;
            border-radius: 8px;
        }}

        .kpi {{ gap: 16px; }}
        .kpi-head {{ display: flex; justify-content: space-between; align-items: flex-start; }}
        .badge {{ padding: 4px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; }}
        .badge-up {{ background: rgba(16,185,129,0.1); color: var(--success); }}
        .mono {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }}
        .muted {{ color: var(--muted); }}
        .section-title {{ display: flex; align-items: center; gap: 10px; margin-bottom: 18px; flex-shrink: 0; }}
        .heatmap {{ display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 8px; flex: 1; align-content: center; }}
        .heat-cell {{ aspect-ratio: 1; border-radius: 8px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead th {{ text-align: left; font-size: 12px; font-weight: 600; padding-bottom: 12px; color: var(--muted); border-bottom: 1px solid var(--border); }}
        tbody tr {{ border-bottom: 1px solid var(--border); }}
        td {{ padding: 16px 0; font-size: 14px; }}
        .active-row {{ background: rgba(255,255,255,0.04); }}
        .chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .chip {{ padding: 4px 8px; border-radius: 999px; font-size: 10px; font-weight: 600; }}
        .chip-technology {{ background: rgba(6,182,212,0.15); color: #06B6D4; }}
        .chip-music {{ background: rgba(245,158,11,0.15); color: #F59E0B; }}
        .chip-fitness {{ background: rgba(16,185,129,0.15); color: #10B981; }}
        .chip-books {{ background: rgba(124,111,247,0.15); color: #7C6FF7; }}
        .btn-primary, .btn-secondary {{ border-radius: 10px; padding: 6px 12px; font-size: 12px; font-weight: 600; border: 1px solid transparent; cursor: pointer; }}
        .btn-primary {{ background: var(--primary); color: white; border-color: var(--primary); }}
        .btn-secondary {{ background: transparent; color: var(--text); border-color: var(--border); }}
        .reco-list {{ display: flex; flex-direction: column; gap: 16px; flex: 1; }}
        .reco-card {{ display: flex; flex-direction: column; gap: 12px; padding: 16px; border-radius: 16px; border: 1px solid var(--border); background: rgba(255,255,255,0.02); }}
        .reco-head {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; }}
        .reco-head h3 {{ margin: 0 0 8px; font-size: 14px; }}
        .success {{ color: var(--success); }}
        .progress {{ width: 100%; height: 6px; border-radius: 999px; overflow: hidden; background: rgba(255,255,255,0.08); }}
        .progress > div {{ height: 100%; border-radius: 999px; background: var(--primary); }}
        .tags-row {{ display: flex; gap: 10px; font-size: 10px; color: var(--muted); }}
        .chip-trend {{ background: rgba(124,111,247,0.1); color: var(--primary); }}
        .sim-grid {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 5px; width: 100%; max-width: 260px; aspect-ratio: 1; margin: 0 auto; flex: 1; align-content: center; }}
        .sim-cell {{ border-radius: 5px; border: 1px solid var(--border); aspect-ratio: 1; }}
        .insight-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; flex: 1; }}
        .insight-card {{ display: flex; gap: 12px; align-items: flex-start; padding: 16px; border-radius: 16px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); }}
        .dot {{ width: 6px; height: 6px; margin-top: 7px; flex-shrink: 0; border-radius: 999px; background: var(--primary); }}

        @media (max-width: 1100px) {{
            .grid-4, .grid-3, .grid-2, .insight-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <!-- ── SIDEBAR ── -->
    <aside class="sidebar">
        <div class="sidebar-brand">
            <div class="brand-icon">✦</div>
            <span>CONTENTAI</span>
        </div>
        <nav class="nav">
            <div class="nav-section-label">Main</div>
            <button class="nav-item active" data-section="overview">
                <span class="nav-icon">◈</span> Overview
                <span class="nav-badge">4</span>
            </button>
            <button class="nav-item" data-section="users">
                <span class="nav-icon">◫</span> Users
            </button>
            <button class="nav-item" data-section="charts">
                <span class="nav-icon">◔</span> Charts
            </button>
            <div class="nav-section-label">Analysis</div>
            <button class="nav-item" data-section="insights">
                <span class="nav-icon">✦</span> AI Insights
            </button>
            <button class="nav-item" data-section="logs">
                <span class="nav-icon">⌘</span> Logs &amp; Matrix
            </button>
        </nav>
        <div class="sidebar-footer">
            <button class="nav-item" id="themeToggle">
                <span class="nav-icon" id="themeIcon">☾</span> Theme
            </button>
        </div>
    </aside>

    <!-- ── MAIN ── -->
    <div class="main">
        <header class="topbar">
            <div class="topbar-title" id="pageTitle">Overview</div>
            <div class="topbar-right">
                <span class="muted" style="font-size:13px;">Target: <strong style="color:var(--primary)">{target_name}</strong></span>
            </div>
        </header>

        <div class="content">

            <!-- SECTION : Overview (KPIs + Heatmap) -->
            <div class="section active" id="section-overview">
                <div class="grid grid-4">
                    <div class="card kpi"><div class="kpi-head"><div class="brand-icon">↗</div><span class="badge badge-up">+12%</span></div><div><div class="muted">Total Users</div><div class="mono" style="font-size:32px;font-weight:600;">50</div></div></div>
                    <div class="card kpi"><div class="kpi-head"><div class="brand-icon">▦</div><span class="badge badge-up">+4%</span></div><div><div class="muted">Recommendations</div><div class="mono" style="font-size:32px;font-weight:600;">247</div></div></div>
                    <div class="card kpi"><div class="kpi-head"><div class="brand-icon">★</div><span class="badge chip-trend">Leading</span></div><div><div class="muted">Top Category</div><div class="mono" style="font-size:32px;font-weight:600;">Fitness</div></div></div>
                    <div class="card kpi"><div class="kpi-head"><div class="brand-icon">◫</div><span class="badge badge-up">+0.8</span></div><div><div class="muted">Avg Activity Score</div><div class="mono" style="font-size:32px;font-weight:600;">4.2</div></div></div>
                </div>
                <div class="spacer"></div>
                <div class="card">
                    <div class="section-title"><div style="color:var(--muted);">◷</div><h2 style="margin:0;font-size:18px;">Activity Heatmap</h2><div style="margin-left:auto;color:var(--muted);font-size:12px;">Last 32 days</div></div>
                    <div class="heatmap">{''.join(heatmap_markup)}</div>
                </div>
            </div>

            <!-- SECTION : Users -->
            <div class="section" id="section-users">
                <div class="grid grid-2">
                    <div class="card">
                        <div class="section-title"><div style="color:var(--muted);">◫</div><h2 style="margin:0;font-size:18px;">Premium Users</h2></div>
                        <table><thead><tr><th>Name</th><th>Age</th><th>Interests</th><th>Score</th><th style="text-align:right;">Action</th></tr></thead><tbody>{''.join(users_markup)}</tbody></table>
                    </div>
                    <div class="card">
                        <div class="section-title"><div style="color:var(--primary);">◎</div><h2 style="margin:0;font-size:18px;">AI Recommendations</h2><span class="badge chip-trend">Target: {target_name}</span></div>
                        <div class="reco-list">{''.join(recommendation_markup)}</div>
                    </div>
                </div>
            </div>

            <!-- SECTION : Charts -->
            <div class="section" id="section-charts">
                <div class="grid grid-2">
                    <div class="card">
                        <div class="section-title"><div style="color:var(--muted);">◔</div><h2 style="margin:0;font-size:18px;">Interest Distribution</h2></div>
                        <div class="chart-wrapper">
                            <img class="chart-img theme-chart" data-dark-src="{categories_dark_path}" data-light-src="{categories_light_path}" src="{categories_dark_path}" alt="Interest distribution" />
                        </div>
                    </div>
                    <div class="card">
                        <div class="section-title"><div style="color:var(--muted);">↗</div><h2 style="margin:0;font-size:18px;">Confidence Trend</h2></div>
                        <div class="chart-wrapper">
                            <img class="chart-img theme-chart" data-dark-src="{scores_dark_path}" data-light-src="{scores_light_path}" src="{scores_dark_path}" alt="Confidence trend" />
                        </div>
                    </div>
                </div>
                <div class="spacer"></div>
                <div class="card">
                    <div class="section-title"><div style="color:var(--muted);">▣</div><h2 style="margin:0;font-size:18px;">Category Treemap</h2></div>
                    <div class="chart-wrapper">
                        <img class="chart-img theme-chart" data-dark-src="{tags_dark_path}" data-light-src="{tags_light_path}" src="{tags_dark_path}" alt="Tag distribution" />
                    </div>
                </div>
            </div>

            <!-- SECTION : AI Insights -->
            <div class="section" id="section-insights">
                <div class="card">
                    <div class="section-title"><div style="color:var(--muted);">✦</div><h2 style="margin:0;font-size:18px;">Generative AI Insights</h2></div>
                    <div class="insight-grid">{insights_markup}</div>
                </div>
            </div>

            <!-- SECTION : Logs & Matrix -->
            <div class="section" id="section-logs">
                <div class="grid grid-2">
                    <div class="card">
                        <div class="section-title"><div style="color:var(--muted);">⌘</div><h2 style="margin:0;font-size:14px;text-transform:uppercase;letter-spacing:0.12em;color:var(--muted);">Analysis Logs</h2></div>
                        <div class="mono muted" style="font-size:13px;display:flex;flex-direction:column;gap:10px;">
                            <div>&gt; Run chi_square_test()</div>
                            <div>x^2 = 12.43</div>
                            <div>p-value = 0.014</div>
                            <div style="color:var(--success);margin-top:6px;">Significant relationship between activity logs and interests detected.</div>
                            <div>_</div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="section-title"><div style="color:var(--muted);">◫</div><h2 style="margin:0;font-size:18px;">User Similarity Matrix</h2></div>
                        <div class="sim-grid">{''.join(similarity_markup)}</div>
                    </div>
                </div>
            </div>

        </div><!-- /content -->
    </div><!-- /main -->

    <script>
        // ── Navigation ──
        const navItems = document.querySelectorAll('.nav-item[data-section]');
        const sections = document.querySelectorAll('.section');
        const pageTitle = document.getElementById('pageTitle');

        const titles = {{
            overview: 'Overview',
            users: 'Users & Recommendations',
            charts: 'Charts',
            insights: 'AI Insights',
            logs: 'Logs & Matrix',
        }};

        navItems.forEach(btn => {{
            btn.addEventListener('click', () => {{
                const target = btn.dataset.section;
                navItems.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                sections.forEach(s => s.classList.remove('active'));
                document.getElementById('section-' + target).classList.add('active');
                pageTitle.textContent = titles[target] || target;
            }});
        }});

        // ── Theme toggle ──
        let dark = true;
        document.getElementById('themeToggle').addEventListener('click', () => {{
            dark = !dark;
            const icon = document.getElementById('themeIcon');
            icon.textContent = dark ? '☾' : '☀';

            document.documentElement.style.setProperty('--bg',      dark ? '#0B1020'                : '#F8FAFC');
            document.documentElement.style.setProperty('--sidebar', dark ? '#0D1424'                : '#F1F5F9');
            document.documentElement.style.setProperty('--card',    dark ? 'rgba(17,24,39,0.94)'   : '#FFFFFF');
            document.documentElement.style.setProperty('--border',  dark ? 'rgba(255,255,255,0.07)': 'rgba(15,23,42,0.08)');
            document.documentElement.style.setProperty('--text',    dark ? '#F8FAFC'               : '#0F172A');
            document.documentElement.style.setProperty('--muted',   dark ? '#94A3B8'               : '#64748B');

            document.querySelectorAll('.theme-chart').forEach(img => {{
                img.src = dark ? img.dataset.darkSrc : img.dataset.lightSrc;
            }});
        }});
    </script>
</body>
</html>
"""