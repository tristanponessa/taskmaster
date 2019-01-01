/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_vec_push.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/04 18:10:57 by trponess          #+#    #+#             */
/*   Updated: 2018/09/25 14:10:20 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	ft_vec_push(t_vector *vec, int n)
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

void	ft_vec_pos_push(t_vector *vec, int index, int n)
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
	vec->arr[index] = n;
	if (index == vec->len)
		vec->len++;
}
