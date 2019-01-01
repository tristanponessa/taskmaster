/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   search.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 17:51:39 by trponess          #+#    #+#             */
/*   Updated: 2018/10/09 16:42:29 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

int		look_for_envvar(char **env, char *str)
{
	int		i;
	char	*word;

	i = 0;
	while (env[i])
	{
		word = stock_word_from_str(env[i][0], '=', env[i]);
		if (ft_strequ(str, word))
			return (i);
		i++;
	}
	return (-1);
}

char	*search_for_command(char *command, char **env_paths)
{
	int		i;
	char	*path;

	i = 0;
	if (access(command, F_OK) == 0 && access(command, X_OK) == 0 \
	&& !opendir(command))
		return (command);
	if (!env_paths)
		return (NULL);
	while (env_paths[i])
	{
		path = add_to_path(env_paths[i], command);
		if (access(path, F_OK) == 0 && access(path, X_OK) == 0)
			return (path);
		i++;
	}
	return (NULL);
}

char	*find_path(char **env, char **part)
{
	int		o;
	int		i;
	char	*path;
	char	*save_current_path;

	i = 0;
	o = 0;
	save_current_path = ft_strnew(ft_strlen(ft_getcwd()));
	ft_strcpy(save_current_path, ft_getcwd());
	translate_path(env, part, &o);
	path = ft_strnew(1);
	ft_strcpy(path, ft_getcwd());
	if (o == -1)
		path = NULL;
	else
		path = ft_strdup(ft_getcwd());
	chdir(save_current_path);
	return (path);
}
