"""Interactive command menu for ANOX."""


def run_cmd_menu():
    """Display comprehensive command reference menu / แสดงเมนูคำสั่งขั้นสูงทั้งหมดของ ANOX"""
    print(
        """
╭──────────────────────────────────────────────────────────────────────────╮
│                    ANOX - Command Reference                              │
│                      All Available Commands                              │
╰──────────────────────────────────────────────────────────────────────────╯

🔐 Authentication & Profile Management
  ═══════════════════════════════════════════════════════════════════════
  anox login              Login and create/select profile
  anox logout             Logout and clear session

💬 Interactive Interfaces
  ═══════════════════════════════════════════════════════════════════════
  anox chat               Interactive AI chat (CLI)
  anox --ui               Workspace + Web interface
                          Options: --ws-port=<port> --webapp-port=<port>
                          VS Code-style with File Explorer, Editor, Terminal, Search
                          Multi-provider AI Copilot support

⚙️  Configuration
  ═══════════════════════════════════════════════════════════════════════
  anox config api         Manage API keys
                          Commands: list, add, edit, delete, import
  anox usage              View and manage token usage
                          Commands: show, summary, reset

🛠️  Development Workflow
  ═══════════════════════════════════════════════════════════════════════
  anox init               Initialize ANOX for this project
  anox analyze            Analyze code for issues
  anox review             Review code quality
  anox fix                Auto-fix detected issues
  anox smartfix           Intelligent auto-fix with AI
  anox status             Show project status

🧪 Testing
  ═══════════════════════════════════════════════════════════════════════
  anox test               Run tests
                          Commands: unit, integration, all, coverage, report

🗂️  Workspace Commands
  ═══════════════════════════════════════════════════════════════════════
  anox workspace          Interactive workspace
  anox workspace test     Test workspace functionality
  anox workspace validate Validate workspace setup
  anox workspace examples Show workspace examples

📱 Mobile & Sync
  ═══════════════════════════════════════════════════════════════════════
  anox mobile             Launch mobile server
  anox sync               Sync data across devices

🔧 Setup & Maintenance
  ═══════════════════════════════════════════════════════════════════════
  anox setup              Initial setup wizard
  anox quickstart         Quick start guide
  anox reset              Reset ANOX state
  anox run                Run ANOX brain CLI

📖 Help & Documentation
  ═══════════════════════════════════════════════════════════════════════
  anox --help             Show comprehensive command reference
  anox cmd                Show this command reference

╭──────────────────────────────────────────────────────────────────────────╮
│ 💡 Quick Start Tips:                                                     │
│                                                                          │
│  First time?     → anox login                                           │
│  Start chatting  → anox chat                                            │
│  Web interface   → anox --ui                                            │
│  Need help?      → anox --help                                          │
╰──────────────────────────────────────────────────────────────────────────╯
"""
    )


if __name__ == '__main__':
    run_cmd_menu()
