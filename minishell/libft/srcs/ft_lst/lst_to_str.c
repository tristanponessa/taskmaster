/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lst_to_str.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/01/16 19:50:13 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*lst_to_str(t_list *list)
{
	int		size;
	char	*str;
	int		cp;

	cp = 0;
	size = lst_len(list);
	str = ft_strnew(size);
	lst_to_limit(&list, 'b');
	while (list)
	{
		str[cp] = list->ch;
		list = list->next;
		cp++;
	}
	return (str);
}
