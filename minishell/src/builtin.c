/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   builtin.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/07/21 17:05:42 by trponess          #+#    #+#             */
/*   Updated: 2018/10/04 17:00:53 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

int		build_in(char *command, char **args, char ***env)
{
	if (ft_strequ(command, "exit"))
	{
		showoff(3);
		ft_free();
		exit(0);
	}
	else if (ft_strequ(command, "env"))
		ft_env(*env, args);
	else if (ft_strequ(command, "echo"))
		ft_echo(args);
	else if (ft_strequ(command, "setenv"))
		*env = ft_setenv(*env, args);
	else if (ft_strequ(command, "unsetenv"))
		*env = ft_unsetenv(*env, args);
	else if (ft_strequ(command, "cd"))
		*env = ft_cd(*env, args);
	else
		return (0);
	return (1);
}

char	**ft_setenv(char **env, char **args)
{
	int i;

	i = 0;
	if (ft_dstrlen(args) != 3)
	{
		ft_printf("error syntax : setenv NAME_OF_ENV_VAR value \n");
		return (env);
	}
	while (env[i])
	{
		if (ft_strnequ(env[i], args[1], ft_strlen(args[1])) &&
			ft_strlen_upto(env[i], '=') == ft_strlen(args[1]))
		{
			env[i] = modify(env[i], args);
			break ;
		}
		i++;
	}
	if (env[i] == 0)
		env = add(env, i, args);
	return (env);
}

char	**ft_unsetenv(char **env, char **args)
{
	int		i;

	i = 0;
	if (ft_dstrlen(args) != 2)
	{
		ft_printf("error syntax : unsetenv NAME_OF_ENV_VAR\n");
		return (env);
	}
	if ((i = look_for_envvar(env, args[1])) != -1)
		env = ft_dstrban(env, args[1]);
	else
		ft_printf("error : env var doesn't exist\n");
	return (env);
}

char	**ft_cd(char **env, char **args)
{
	int i;
	int j;

	i = look_for_envvar(env, "PWD");
	j = look_for_envvar(env, "OLDPWD");
	if (chdir(args[1]) == -1)
	{
		ft_printf("cd: no such file or directory: %s\n", args[1]);
		return (env);
	}
	env[j] = ft_strjoin_multi("OLD", env[i], "", "");
	env[i] = ft_strjoin_multi("PWD=", ft_getcwd(), "", "");
	return (env);
}

void	ft_env(char **env, char **args)
{
	int i;
	int j;

	i = 1;
	if (ft_dstrlen(args) == 1)
	{
		ft_putdstr(env);
		return ;
	}
	while (i < ft_dstrlen(args))
	{
		if ((j = look_for_envvar(env, args[i])) > -1)
			ft_printf("%s\n", env[j]);
		else
			ft_printf("error : env var <%s> doesn't exist\n", args[i]);
		i++;
	}
}
