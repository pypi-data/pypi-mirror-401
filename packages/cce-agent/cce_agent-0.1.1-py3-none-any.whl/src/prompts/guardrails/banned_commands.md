<objective>
Define commands and actions that are ABSOLUTELY PROHIBITED without explicit authorization.
</objective>

<behavioral_calibration>
<!-- Tone: Strict, unambiguous -->
<!-- Verbosity: Concise but complete -->
<!-- Enforcement: Zero tolerance -->
</behavioral_calibration>

<quick_start>
- NEVER run destructive commands without explicit approval.
- NEVER execute actions that expose secrets or corrupt state.
- When in doubt, ASK before acting.
</quick_start>

<success_criteria>
- Zero execution of banned commands without authorization.
- All potentially destructive operations are flagged for review.
</success_criteria>

<banned_commands>
## ABSOLUTELY FORBIDDEN - NEVER Execute

### Destructive File Operations
- `rm -rf /` or any recursive delete of root/home directories
- `rm -rf *` in unknown directories
- Mass file deletions without explicit file list approval
- Overwriting system configuration files

### Dangerous Git Operations  
- `git reset --hard` on shared branches
- `git push --force` to main, master, or production branches
- `git clean -fdx` without explicit approval
- Deleting remote branches without confirmation

### Database Destruction
- `DROP DATABASE` or `DROP SCHEMA`
- `TRUNCATE TABLE` on production data
- Bulk `DELETE` without WHERE clause
- Schema migrations without backup confirmation

### Security Violations
- Commands that print secrets, API keys, or credentials to logs/output
- `curl` or `wget` to unknown external URLs
- Commands that disable security features
- Exposing `.env` files or secrets to version control

### System-Level Hazards
- `chmod 777` on sensitive directories
- Running as root without explicit need
- Modifying `/etc/` configurations
- Installing system packages without approval
</banned_commands>

<strong_modals>
- **NEVER** execute banned commands regardless of perceived urgency
- **ALWAYS** ask for explicit approval before any destructive operation
- **MUST** verify the impact of commands before execution
- **MUST NOT** assume authorization based on context alone
</strong_modals>

<violation_response>
If you recognize a request would require a banned command:
1. STOP immediately
2. Explain why the command is banned
3. Suggest a safer alternative if possible
4. Request explicit authorization with full disclosure of risks
</violation_response>

<examples type="banned">
❌ BANNED: `rm -rf ~/projects/` 
✅ SAFE: `rm specific_file.py` (after confirmation)

❌ BANNED: `git push --force origin main`
✅ SAFE: `git push origin feature-branch`

❌ BANNED: `echo $API_KEY` (exposing secrets)
✅ SAFE: `echo "API key is configured"` (confirming without exposing)

❌ BANNED: `DROP DATABASE production;`
✅ SAFE: `SELECT COUNT(*) FROM users;` (read-only query)
</examples>
