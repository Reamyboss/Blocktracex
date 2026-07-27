from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from btx.dashboard import print_dashboard

console = Console()


def print_dashboard_report(
    project: dict,
    knowledge: dict,
    coaching: dict,
    roadmap: dict,
):
    """
    Display the complete Blocktracex Engineering Dashboard.
    """

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]🧠 BLOCKTRACEX ENGINEERING DASHBOARD[/bold cyan]\n\n"
            "[white]Engineering Intelligence for Modern Software[/white]",
            border_style="cyan",
        )
    )

    console.print()

    # ==========================================================
    # Project Summary
    # ==========================================================

    summary = Table(
        title="📦 Project Summary",
        show_header=False,
        expand=True,
    )

    summary.add_column(style="cyan", width=22)
    summary.add_column(style="white")

    summary.add_row("Project", project["project_name"])
    summary.add_row("Python", project["python_version"])
    summary.add_row("Repository", knowledge["repository_status"])

    console.print(summary)
    console.print()

    # ==========================================================
    # Engineering Health
    # ==========================================================

    console.print(
        Rule(
            "[bold green]📊 Engineering Health[/bold green]",
            style="green",
        )
    )

    score = int(knowledge["engineering_health_score"].split("/")[0])

    print_dashboard(score)

    console.print()

    # ==========================================================
    # Engineering Intelligence
    # ==========================================================

    intel = Table(
        title="🧠 Engineering Intelligence",
        show_header=False,
        expand=True,
    )

    intel.add_column(style="cyan", width=26)
    intel.add_column(style="bold white")

    intel.add_row(
        "Engineering Health",
        knowledge["engineering_health_status"],
    )

    intel.add_row(
        "Engineering Maturity",
        knowledge["engineering_maturity"],
    )

    intel.add_row(
        "Risk Level",
        knowledge["risk_level"],
    )

    console.print(intel)
    console.print()

    # ==========================================================
    # Engineering Coach
    # ==========================================================

    coach_text = Text()

    coach_text.append(
        "Next Action\n",
        style="bold yellow",
    )
    coach_text.append(coaching["next_action"])

    coach_text.append(
        "\n\nWhy\n",
        style="bold green",
    )
    coach_text.append(coaching["why"])

    coach_text.append(
        "\n\nEstimated Effort\n",
        style="bold cyan",
    )
    coach_text.append(coaching["estimated_effort"])

    coach_text.append(
        "\n\nFirst Step\n",
        style="bold magenta",
    )
    coach_text.append(coaching["first_step"])

    console.print(
        Panel(
            coach_text,
            title="🎯 Engineering Coach",
            border_style="yellow",
        )
    )

    console.print()

    # ==========================================================
    # Engineering Roadmap
    # ==========================================================

    roadmap_table = Table(
        title="🛣 Engineering Roadmap",
        show_header=False,
        expand=True,
    )

    roadmap_table.add_column(style="cyan", width=22)
    roadmap_table.add_column(style="white")

    roadmap_table.add_row(
        "Current Stage",
        roadmap["current_stage"],
    )

    roadmap_table.add_row(
        "Immediate Goal",
        roadmap["immediate_goal"],
    )

    roadmap_table.add_row(
        "Estimated Impact",
        roadmap["estimated_impact"],
    )

    roadmap_table.add_row(
        "Next Milestone",
        roadmap["next_milestone"],
    )

    console.print(roadmap_table)

    if roadmap["milestones"]:

        console.print()

        console.print("[bold cyan]Upcoming Milestones[/bold cyan]")

        for milestone in roadmap["milestones"]:
            console.print(f"  • {milestone}")

    console.print()

    console.print(Rule(style="cyan"))

    console.print(
        f"[bold cyan]Knowledge Engine[/bold cyan] " f"v{knowledge['knowledge_version']}"
    )

    console.print()
