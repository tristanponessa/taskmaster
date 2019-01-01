/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_vec_push.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/04 18:10:57 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void		ft_vec_push(t_vector *vec, int n)
{
	int *tmp;

	if (vec->len == vec->cap)
	{
		tmp = vec->arr;
		vec->arr = ft_arrnew(vec->cap * 2);
		ft_memcpy(vec->arr, tmp, vec->len * sizeof(int));
		free(tmp);
		vec->cap *= 2;
	}
	vec->arr[vec->len] = n;
	vec->len++;
}
