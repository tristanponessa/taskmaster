/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_create_double_str.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/28 19:59:04 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	**ft_create_double_str(int y, int x)
{
	char	**tab;
	int		i;
	int		j;
	int		k;

	tab = (char**)malloc(sizeof(char*) * (y + 1));
	i = 0;
	j = 0;
	while (j < y)
	{
		k = 0;
		tab[j] = (char*)malloc(sizeof(char) * (x + 1));
		while (k < x)
		{
			tab[j][k] = '\0';
			i++;
			k++;
		}
		tab[j][k] = '\0';
		j++;
	}
	tab[j] = 0;
	return (tab);
}
