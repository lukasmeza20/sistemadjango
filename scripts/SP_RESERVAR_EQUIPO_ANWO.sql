USE [base_datos]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF (OBJECT_ID('SP_RESERVAR_EQUIPO_ANWO', 'P') IS NOT NULL) DROP PROCEDURE [dbo].[SP_RESERVAR_EQUIPO_ANWO]
GO
CREATE PROCEDURE [dbo].[SP_RESERVAR_EQUIPO_ANWO]
    @nroserieanwo NVARCHAR(100),
	@reservado NVARCHAR(1)
AS
BEGIN
	/*
		Ejemplos de ejecucion del procedimiento:
		
        EXEC SP_RESERVAR_EQUIPO_ANWO 'A9', 'S'
        SELECT * FROM AnwoStockProducto WHERE nroserieanwo = 'A9' --DEBE ENTREGAR UNA FILA CON reservado = 'S'

		EXEC SP_RESERVAR_EQUIPO_ANWO 'A9', 'N'
        SELECT * FROM AnwoStockProducto WHERE nroserieanwo = 'A9' --DEBE ENTREGAR UNA FILA CON reservado = 'N'
	*/

    SET NOCOUNT ON;

    UPDATE AnwoStockProducto
    SET reservado = @reservado
    WHERE nroserieanwo = @nroserieanwo;
END
GO