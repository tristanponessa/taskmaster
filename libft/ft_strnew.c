/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:26:31 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:04:09 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnew(size_t size)
{
	char *zone;

	zone = (char *)malloc(sizeof(char) * (size + 1));
	if (!zone)
		return (NULL);
	ft_memset(zone, '\0', size + 1);
	return (zone);
}
