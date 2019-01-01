/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strsub.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:27:09 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:04:32 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strsub(char const *s, unsigned int start, size_t len)
{
	unsigned int	i;
	char			*bus;

	bus = (char *)malloc(sizeof(char) * (len + 1));
	if (!bus || !s)
		return (NULL);
	i = 0;
	while (i < len)
	{
		bus[i] = s[start];
		i++;
		start++;
	}
	bus[i] = '\0';
	return (bus);
}
