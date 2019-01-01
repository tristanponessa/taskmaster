/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   path.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/23 17:59:48 by trponess          #+#    #+#             */
/*   Updated: 2018/09/26 18:10:27 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

char	*add_to_path(char *path, char *rest)
{
	char *new_path;

	new_path = ft_strjoin(path, "/");
	new_path = ft_strjoin(new_path, rest);
	return (new_path);
}

char	*find_parent(char *path)
{
	int		i;
	char	*parent;

	end_str(path, &i);
	if (!ft_strfind(path, '/'))
		return (path);
	parent = ft_strnew(ft_strlen(path));
	while (i >= 0 && path[i] != '/')
		i--;
	path[i] = '\0';
	i = 0;
	while (path[i])
	{
		parent[i] = path[i];
		i++;
	}
	return (parent);
}

char	*ft_getcwd(void)
{
	char *s;
	char *n;

	n = ft_strnew(1);
	n = getcwd(NULL, 0);
	s = ft_strnew(1);
	s = ft_strjoin(s, n);
	free(n);
	return (s);
}

char	*double_period_pattern(char *args)
{
	char	**part;
	char	*path;
	int		i;
	int		j;

	i = 0;
	j = 0;
	path = ft_strnew(1);
	part = ft_split_spaces(args, '/');
	while (part[i])
	{
		if (ft_strequ(part[i], ".."))
			i++;
		else
			return (0);
	}
	part = ft_split_spaces(ft_getcwd(), '/');
	part[0] = ft_strjoin("/", part[0]);
	while (j < ft_dstrlen(part) - i)
	{
		path = ft_strjoin_multi(path, part[j], "/", "");
		j++;
	}
	path[ft_strlen(path) - 1] = '\0';
	return (path);
}
