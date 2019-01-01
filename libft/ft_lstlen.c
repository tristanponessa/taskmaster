/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/23 17:49:44 by trponess          #+#    #+#             */
/*   Updated: 2017/11/23 19:37:48 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_lstlen(t_list *elem)
{
	size_t len;

	len = 0;
	while (elem && elem->next)
	{
		len++;
		elem = elem->next;
	}
	return (len);
}
