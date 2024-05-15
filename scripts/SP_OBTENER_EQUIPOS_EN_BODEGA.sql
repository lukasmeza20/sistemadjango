USE [base_datos]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_OBTENER_EQUIPOS_EN_BODEGA', 'P') IS NOT NULL) DROP PROCEDURE [dbo].[SP_OBTENER_EQUIPOS_EN_BODEGA]
GO
CREATE PROCEDURE [dbo].[SP_OBTENER_EQUIPOS_EN_BODEGA]
AS
BEGIN
	SET NOCOUNT ON;

    SELECT
		s.idstock, p.idprod, p.nomprod, f.nrofac, 
		CASE 
			WHEN f.nrofac IS NOT NULL 
			THEN 'Vendido'
			ELSE 'En bodega'
		END AS 'estado'
	FROM 
		StockProducto s 
		INNER JOIN Producto p ON s.idprod = p.idprod
		LEFT OUTER JOIN Factura  f ON s.nrofac = f.nrofac
END
GO