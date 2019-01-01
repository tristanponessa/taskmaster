/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   prepare.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 17:16:31 by trponess          #+#    #+#             */
/*   Updated: 2018/10/09 17:12:49 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

char	**prepare_args(void)
{
	char **args;
	char *line;

	line = NULL;
	if (!get_next_line(0, &line))
	{
		ft_printf("\n\nexited minishell by ctrl+D\n");
		showoff(3);
		ft_free();
		exit(0);
	}
	args = NULL;
	args = ft_split_most_wanted(line,\
			ft_split_spaces(" +\t", '+'), '*', "\"\"");
	args = ft_strict_dstr(args);
	return (args);
}

void	translate_path(char **env, char **part, int *o)
{
	int p;

	p = 0;
	while (part[p])
	{
		if (ft_strequ(part[p], "."))
			*o = chdir(ft_getcwd());
		else if (ft_strequ(part[p], ".."))
			*o = chdir(find_parent(ft_getcwd()));
		else if (ft_strequ(part[p], "~") || ft_strequ(part[p], "home"))
		{
			*o = chdir(ft_strjoin(ft_getcwd(), \
			&env[look_for_envvar(env, "HOME")][5]));
			if (p == 0)
				*o = chdir(&env[look_for_envvar(env, "HOME")][5]);
		}
		else if (part[p][0] == '$')
			*o = chdir(ft_strjoin(ft_getcwd(), translate_var(env, part[p])));
		else
			*o = chdir(ft_strjoin_multi(ft_getcwd(), "/", part[p], ""));
		if (*o == -1)
			return ;
		p++;
	}
}

char	*translate_symbol(char **env, char *args, char *tmp)
{
	if (ft_strequ(args, ".."))
		args = ft_strdup(&find_parent(tmp)[4]);
	if (ft_strequ(args, "."))
		args = ft_strdup(&env[look_for_envvar(env, "PWD")][4]);
	if (ft_strequ(args, "~") || ft_strequ(args, "home"))
		args = ft_strdup(&env[look_for_envvar(env, "HOME")][5]);
	if (args[0] == '$')
		args = translate_var(env, args);
	return (args);
}

char	**translate_av(char **env, char **original_env, char **args)
{
	int		x;
	char	*tmp;

	if (!args[0])
		return (NULL);
	x = 1;
	env = if_pwds_empty(env, original_env);
	tmp = ft_strdup(env[look_for_envvar(env, "PWD")]);
	while (args[x])
	{
		if (ft_strfind(args[x], '/'))
		{
			if ((tmp = find_path(env, ft_split_spaces(args[x], '/'))))
				args[x] = ft_strdup(tmp);
		}
		else
		{
			args[x] = translate_symbol(env, args[x], tmp);
			if (ft_strequ(args[0], "cd") && ft_strequ(args[x], "-"))
				args[x] = ft_strdup(&env[look_for_envvar(env, "OLDPWD")][7]);
		}
		x++;
	}
	return (args);
}
