USE [base_datos]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_TODOS_LOS_USUARIOS', 'P') IS NOT NULL) DROP PROCEDURE [dbo].[SP_OBTENER_TODOS_LOS_USUARIOS]
GO
CREATE PROCEDURE [dbo].[SP_OBTENER_TODOS_LOS_USUARIOS]
AS
BEGIN
	SET NOCOUNT ON;
	
	SELECT 
		*
	FROM 
		PerfilUsuario per
		INNER JOIN auth_user usu ON per.user_id = usu.id
END