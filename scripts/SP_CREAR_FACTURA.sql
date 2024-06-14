USE [base_datos]
GO
/****** Object:  StoredProcedure [dbo].[SP_CREAR_FACTURA]    Script Date: 30-05-2024 14:53:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SP_CREAR_FACTURA]

    @descfac        VARCHAR(100),
    @monto          INT,
    @rutcli         VARCHAR(20),
    @idprod         INT
AS
BEGIN
    DECLARE @tiposol VARCHAR(100)
    SET @tiposol = 'Instalación';

    DECLARE @nrofac AS INT
    SET @nrofac = (SELECT ISNULL(MAX(nrofac), 0) + 1 FROM FACTURA)

    INSERT INTO Factura(nrofac, rutcli, idprod, fechafac, descfac, monto)
    VALUES (
        @nrofac,
        @rutcli,
        @idprod,
        GETDATE(),
        @descfac,
        @monto
    )

    IF (@tiposol = 'Instalación')
    BEGIN
        INSERT INTO GuiaDespacho (nrogd, estadogd, idprod, nrofac)
        VALUES (
            (SELECT ISNULL(MAX(nrogd), 0) + 1 FROM GuiaDespacho),
            'En bodega',
            @idprod,
            @nrofac
        )
    END

    INSERT INTO SolicitudServicio(nrosol, tiposol, fechavisita, descsol, estadosol, nrofac, ruttec)
    VALUES (
        (SELECT ISNULL(MAX(nrosol), 0) + 1 FROM SolicitudServicio),
        @tiposol,
        GETDATE(),
        @tiposol,
        'Aceptada',
        @nrofac,
        '6666-6'
    )
END


