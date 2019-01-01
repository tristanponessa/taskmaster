/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:22:24 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:03:40 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dest, const char *src, size_t size)
{
	size_t i;
	size_t j;

	i = 0;
	j = 0;
	while (dest[j] && j < size)
		j++;
	while (src[i] && i + j + 1 < size)
	{
		dest[i + j] = src[i];
		i++;
	}
	if (j != size)
		dest[i + j] = '\0';
	return (j + ft_strlen(src));
}
