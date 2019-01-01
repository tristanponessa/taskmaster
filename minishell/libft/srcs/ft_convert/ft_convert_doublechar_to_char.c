/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_doublechar_to_char.c                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/29 02:05:44 by tristan           #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*convert_doublechar_to_char(char **tab)
{
	char		*str;
	t_counter	c;
	int			full_size;

	full_size = 0;
	ft_bzero(&c, sizeof(t_counter));
	while (tab[++(c.i)])
		full_size = full_size + ft_strlen(tab[c.i]);
	str = ft_strnew(full_size);
	c.i = 0;
	while (tab[c.i])
	{
		while (tab[c.i][c.j])
			str[(c.k)++] = tab[c.i][(c.j)++];
		c.j = 0;
		c.i++;
	}
	return (str);
}
