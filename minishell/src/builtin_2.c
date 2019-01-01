/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   builtin_2.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 18:08:12 by trponess          #+#    #+#             */
/*   Updated: 2018/09/27 18:18:24 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

void	ft_echo(char **args)
{
	int i;

	i = 1;
	while (args[i])
	{
		ft_printf("%s", args[i++]);
		if (args[i])
			ft_putchar(' ');
	}
	if (ft_dstrlen(args) > 1)
		ft_putchar('\n');
}

char	**ft_resetenv(char **env, char **original_env, char **args)
{
	int		i;
	char	*save;

	i = 0;
	while (env[i])
	{
		if (ft_strnequ(env[i], args[1], ft_strlen(args[1])) &&
		ft_strlen_upto(env[i], '=') == ft_strlen(args[1]))
		{
			save = ft_strdup(env[i]);
			ft_strcpy(env[i], original_env[i]);
			ft_printf("modified\n %s -> %s\n", save, env[i]);
			break ;
		}
		i++;
	}
	if (env[i] == 0)
		ft_printf("error : env var doesn't exist\n");
	return (env);
}
