#include "atheme-compat.h"

DECLARE_MODULE_V1
(
	"contrib/ircd_funserv", false, _modinit, _moddeinit,
	PACKAGE_STRING,
	"Sam Dodrill <shadow.h511@gmail.com>"
);

#define BOTNAME "ShadowNET"

service_t *funserv;

static void funserv_cmd_requestbot(sourceinfo_t *si, int parc, char *parv[]);
static void funserv_cmd_help(sourceinfo_t *si, int parc, char *parv[]);

command_t funserv_requestbot = { "REQUESTBOT", "Requests the network extended services bot to your channel.",
				AC_NONE, 1, funserv_cmd_requestbot, { .path = "" } };
command_t funserv_help = { "HELP", "Displays contextual help information.",
				AC_NONE, 1, funserv_cmd_help, { .path = "help" } };

void _modinit(module_t *m)
{
	funserv = service_add("funserv", NULL);

	service_bind_command(funserv, &funserv_requestbot);
	service_bind_command(funserv, &funserv_help);
}

void _moddeinit(module_unload_intent_t intent)
{
	service_unbind_command(funserv, &funserv_requestbot);
	service_unbind_command(funserv, &funserv_help);

	service_delete(funserv);
}

static void funserv_cmd_requestbot(sourceinfo_t *si, int parc, char *parv[])
{
	char *name = parv[0];
	mychan_t *mc;

	if (!name)
	{
		command_fail(si, fault_needmoreparams, STR_INSUFFICIENT_PARAMS, "REQUESTBOT");
		command_fail(si, fault_needmoreparams, _("Syntax: REQUESTBOT <#channel>"));
	}

	if (*name != '#')
	{
		command_fail(si, fault_needmoreparams, STR_INVALID_PARAMS, "REQUESTBOT");
		command_fail(si, fault_needmoreparams, _("Syntax: REQUESTBOT <#channel>"));
	}

	if (!(mc = mychan_find(name)))
	{
		command_fail(si, fault_nosuch_target, _("Channel \2%s\2 is not registered."), name);
		return;
	}

	if (!is_founder(mc, entity(si->smu)))
	{
		command_fail(si, fault_noprivs, _("You are not authorized to perform this operation."));
		return;
	}

	myuser_notice(funserv->nick, myuser_find_ext(BOTNAME), "JOIN %s", name);

	command_success_nodata(si, "The bot should now be in %s.", name);
}

static void funserv_cmd_help(sourceinfo_t *si, int parc, char *parv[])
{
	command_help(si, si->service->commands);
}

/* vim:cinoptions=>s,e0,n0,f0,{0,}0,^0,=s,ps,t0,c3,+s,(2s,us,)20,*30,gs,hs
 * vim:ts=8
 * vim:sw=8
 * vim:noexpandtab
 */
