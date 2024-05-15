USE [base_datos]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_SOLICITUDES_DE_SERVICIO', 'P') IS NOT NULL) DROP PROCEDURE [dbo].[SP_OBTENER_SOLICITUDES_DE_SERVICIO]
GO
CREATE PROCEDURE [dbo].[SP_OBTENER_SOLICITUDES_DE_SERVICIO]
	@tipousu VARCHAR(50),
	@rut     VARCHAR(50)
AS
BEGIN
	/*
		Ejemplos de ejecucion del procedimiento:
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '6666-6'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '7777-7'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '8888-8'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Cliente', '1111-1'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Todos', ''
	*/

	SET NOCOUNT ON;

	IF (@tipousu = 'Técnico')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		WHERE
			pertec.rut = @rut
		ORDER BY 
			usucli.first_name

	IF (@tipousu = 'Cliente')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		WHERE
			percli.rut = @rut
		ORDER BY 
			usutec.first_name

	IF (@tipousu = 'Todos')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		ORDER BY
			usucli.first_name,
			usutec.first_name

END
GO