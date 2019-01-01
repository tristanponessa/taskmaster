/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:22:24 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int	ft_strlcat(char *dest, const char *src, int size)
{
	int i;
	int j;

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
