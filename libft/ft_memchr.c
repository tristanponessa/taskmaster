/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:00:58 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:01:54 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	size_t		i;
	const char	*ch_s;

	ch_s = (const char*)s;
	i = 0;
	while (i < n)
	{
		if (ch_s[i] == (char)c)
			return ((void*)(s + i));
		i++;
	}
	return (NULL);
}
