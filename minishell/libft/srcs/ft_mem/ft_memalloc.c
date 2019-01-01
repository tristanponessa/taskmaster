/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memalloc.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tristan <tristan@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 17:57:58 by trponess          #+#    #+#             */
/*   Updated: 2018/09/12 10:35:27 by tristan          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	*ft_memalloc(int size)
{
	void *zone;

	zone = ft_strnew(size);
	if (!zone)
		return (NULL);
	ft_memset(zone, '\0', size);
	return (zone);
}
