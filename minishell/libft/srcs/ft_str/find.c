/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   find.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/07/18 14:14:32 by tristan           #+#    #+#             */
/*   Updated: 2018/09/24 16:27:24 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int		ft_strfind(char *str, char ch)
{
	int i;

	i = 0;
	while (str[i])
	{
		if (str[i] == ch)
			return (1);
		i++;
	}
	return (0);
}

int		ft_strfind_pos(char *str, char ch)
{
	int i;

	i = 0;
	while (str[i])
	{
		if (str[i] == ch)
			return (i);
		i++;
	}
	return (-1);
}

int		ft_dstr_find_str(char **separator, char *to_find)
{
	int k;

	k = 0;
	while (separator[k])
	{
		if (ft_strncmp(separator[k], to_find, ft_strlen(separator[k])) == 0)
			return (ft_strlen(separator[k]));
		k++;
	}
	return (0);
}
