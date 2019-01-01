/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   prepare_extra.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 17:25:55 by trponess          #+#    #+#             */
/*   Updated: 2018/09/24 18:04:14 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

char	*translate_var(char **env, char *args)
{
	int u;

	u = look_for_envvar(env, &args[1]);
	if (u == -1)
		ft_printf("error : <%s> env var doesn't exist\n", args);
	else
	{
		args = ft_stradd(args, ft_strlen(env[u]));
		ft_strcpy(args, &env[u][ft_strlen_upto(env[u], '=') + 1]);
	}
	return (args);
}

char	**if_pwds_empty(char **env, char **original_env)
{
	int i;
	int j;

	i = look_for_envvar(env, "PWD");
	j = look_for_envvar(env, "OLDPWD");
	if (ft_strequ(env[i], "PWD=(null)"))
		env[i] = ft_strdup(original_env[i]);
	if (ft_strequ(env[j], "OLDPWD=(null)"))
		env[j] = ft_strdup(original_env[j]);
	return (env);
}
