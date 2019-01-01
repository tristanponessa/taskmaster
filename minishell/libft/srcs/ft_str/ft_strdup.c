/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/24 17:20:12 by trponess          #+#    #+#             */
/*   Updated: 2018/09/24 17:20:15 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*ft_strdup(const char *src)
{
	int		i;
	char	*copy;

	i = 0;
	copy = ft_strnew(ft_strlen(src));
	if (!copy)
		return (NULL);
	i = 0;
	while (src[i])
	{
		copy[i] = src[i];
		i++;
	}
	copy[i] = '\0';
	return (copy);
}

char	**ft_dstrdup(char **src)
{
	char	**copy;
	int		i;

	i = 0;
	copy = ft_dstrnew(ft_dstrlen(src), 1);
	if (!copy || !src)
		return (NULL);
	while (copy[i])
	{
		copy[i] = ft_strjoin(copy[i], src[i]);
		i++;
	}
	copy[i] = 0;
	return (copy);
}
