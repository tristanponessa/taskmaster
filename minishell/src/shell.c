/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   shell.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 17:24:57 by trponess          #+#    #+#             */
/*   Updated: 2018/10/09 17:05:10 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

char	**save(char **env, char **args, int save)
{
	static char **original_env;
	static char **original_args;

	if (save == 1)
		original_env = ft_dstrdup(env);
	if (save == 2)
		original_args = ft_dstrdup(args);
	if (save == -1)
		return (original_env);
	if (save == -2)
		return (original_args);
	return (NULL);
}

void	create_process(char *dir, char **args, char **ev)
{
	pid_t	pid;
	int		status;

	pid = fork();
	if (pid == 0)
		execve(dir, args, ev);
	if (pid)
		wait(&status);
}

char	**pwd_check(char **ev)
{
	char **tmp;

	tmp = ft_dstrnew(3, 1);
	if (look_for_envvar(ev, "PWD") == -1)
	{
		tmp[0] = ft_strjoin(tmp[0], "setenv");
		tmp[1] = ft_strjoin(tmp[1], "PWD");
		tmp[2] = ft_strjoin(tmp[2], ft_getcwd());
		ev = ft_setenv(ev, tmp);
	}
	if (look_for_envvar(ev, "OLDPWD") == -1)
	{
		tmp[0] = ft_strjoin(tmp[0], "setenv");
		tmp[1] = ft_strjoin(tmp[1], "OLDPWD");
		tmp[2] = ft_strjoin(tmp[2], find_parent(ft_getcwd()));
		ev = ft_setenv(ev, tmp);
	}
	return (ev);
}

char	**home_check(char **ev)
{
	char **tmp;
	char **origin_env;

	tmp = ft_dstrnew(3, 1);
	if (look_for_envvar(ev, "HOME") == -1)
	{
		origin_env = save(NULL, NULL, -1);
		tmp[0] = ft_strjoin(tmp[0], "setenv");
		tmp[1] = ft_strjoin(tmp[1], "HOME");
		tmp[2] = ft_strjoin(tmp[2], \
		&origin_env[look_for_envvar(origin_env, "HOME")][5]);
		ev = ft_setenv(ev, tmp);
	}
	return (ev);
}

void	shell_runs(char **ev, char **ev_c)
{
	char **args;
	char *dir;

	while (1)
	{
		if (look_for_envvar(ev, "PATH") > -1)
			ev_c = ft_split_spaces(&ev[look_for_envvar(ev, "PATH")][5], ':');
		else
			ev_c = NULL;
		ev = pwd_check(ev);
		ev = home_check(ev);
		ft_printf("[%s%s%s]$>", KPUR, ft_getcwd(), KNRM);
		args = prepare_args();
		if (args[0])
			args = translate_av(ev, save(NULL, NULL, -1), args);
		if (!args[0])
			ft_printf("enter a command\n");
		else if (build_in(args[0], args, &ev))
			;
		else if ((dir = search_for_command(args[0], ev_c)))
			create_process(dir, args, ev);
		else
			ft_printf("command not found : <%s>\n", args[0]);
	}
}
