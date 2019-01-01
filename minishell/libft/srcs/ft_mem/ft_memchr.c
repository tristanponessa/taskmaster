/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:00:58 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	*ft_memchr(const void *s, int c, int n)
{
	int			i;
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
