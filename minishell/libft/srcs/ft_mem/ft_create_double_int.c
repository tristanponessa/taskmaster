/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_create_double_int.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/28 20:03:07 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int		**ft_create_double_int(int y, int x)
{
	int		**tab;
	int		i;
	int		j;
	int		k;

	tab = (int**)malloc(sizeof(int*) * y);
	i = 0;
	j = 0;
	while (j < y)
	{
		k = 0;
		tab[j] = (int*)malloc(sizeof(int) * x);
		while (k < x)
		{
			tab[j][k] = 0;
			i++;
			k++;
		}
		j++;
	}
	tab[j] = 0;
	return (tab);
}
