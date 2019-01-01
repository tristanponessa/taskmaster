/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:26:31 by trponess          #+#    #+#             */
/*   Updated: 2018/09/25 14:05:52 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*ft_strnew(int size)
{
	char *zone;

	zone = (char *)malloc(sizeof(char) * (size + 1));
	if (!zone)
		return (NULL);
	ft_memset(zone, '\0', size + 1);
	ft_leak_collector(zone, "save");
	return (zone);
}
