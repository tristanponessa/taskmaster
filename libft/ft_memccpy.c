/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memccpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 17:58:21 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:01:50 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memccpy(void *dst, const void *src, int c, size_t n)
{
	size_t			i;
	unsigned char	x;

	x = (unsigned char)c;
	i = 0;
	while (i < n)
	{
		if ((((unsigned char*)dst)[i] = ((unsigned char*)src)[i]) == x)
			return (&dst[i + 1]);
		i++;
	}
	return (NULL);
}
