/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strsub.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:27:09 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*ft_strsub(char const *s, unsigned int start, int len)
{
	int				i;
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
