/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sqrt.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/07/10 20:07:50 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int		ft_sqrt(int nb)
{
	int racine;
	int sqr;

	racine = 1;
	sqr = 0;
	while (racine <= nb / 2)
	{
		sqr = racine * racine;
		if (sqr == nb)
			return (racine);
		racine = racine + 1;
	}
	return (-1);
}
