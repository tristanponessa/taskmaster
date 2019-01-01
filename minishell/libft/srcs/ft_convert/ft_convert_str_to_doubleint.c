/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_convert_str_to_doubleint.c                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/01 18:08:59 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int		**ft_convert_str_to_doubleint(char *str, int width, int height)
{
	t_counter	c;
	int			**map;
	char		temp[13];

	map = ft_darrnew(height, width);
	ft_bzero(&c, sizeof(t_counter));
	while (str[c.l++])
	{
		if (ft_isdigit(str[c.l]) || (str[c.l] == '-'))
		{
			ft_bzero(temp, 13);
			c.h = 0;
			while (ft_isdigit(str[c.l]) == 1 || (str[c.l] == '-'))
				temp[c.h++] = str[c.l++];
			map[c.i][c.k++] = ft_atoi(temp);
			if (c.k == width)
			{
				c.i++;
				c.k = 0;
			}
		}
	}
	return (map);
}
