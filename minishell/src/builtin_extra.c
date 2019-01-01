/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   builtin_extra.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 17:59:06 by trponess          #+#    #+#             */
/*   Updated: 2018/09/24 17:54:32 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

char	*modify(char *env, char **args)
{
	char *save;

	save = ft_strdup(env);
	env = ft_strjoin_multi(args[1], "=", args[2], "");
	ft_printf("modified :\n %s -> %s\n", save, env);
	return (env);
}

char	**add(char **env, int i, char **args)
{
	char **tmp;

	tmp = ft_dstrnew(1, ft_strlen(args[1]) + ft_strlen(args[2]) + 1);
	tmp[0] = ft_strjoin_multi(args[1], "=", args[2], "");
	env = ft_dstrjoin(env, tmp);
	ft_printf("created :\n  %s\n", env[i]);
	return (env);
}
