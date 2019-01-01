/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memccpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 17:58:21 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	*ft_memccpy(void *dst, const void *src, int c, int n)
{
	int				i;
	unsigned char	x;

	x = (unsigned char)c;
	i = 0;
	while (i < n)
	{
		if ((((unsigned char*)dst)[i] = ((unsigned char*)src)[i]) == x)
			return (NULL);
		i++;
	}
	return (NULL);
}
