USE [base_datos]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_FACTURAS', 'P') IS NOT NULL) DROP PROCEDURE [dbo].[SP_OBTENER_FACTURAS]
GO
CREATE PROCEDURE [dbo].[SP_OBTENER_FACTURAS]
	@rut     VARCHAR(50)
AS	
BEGIN
	SELECT 
			fac.nrofac, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			fac.fechafac,
			fac.descfac,
			fac.monto,
			gd.nrogd,
			gd.estadogd,
			sol.nrosol,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
			LEFT JOIN GuiaDespacho  gd     ON gd.nrofac = fac.nrofac
		WHERE
			percli.rut = ISNULL(@rut,percli.rut)
		ORDER BY 
			usucli.first_name
END
GO
