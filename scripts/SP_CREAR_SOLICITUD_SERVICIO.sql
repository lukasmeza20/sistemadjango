SET ANSI_NULLS ON 
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE SP_CREAR_SOLICITUD_SERVICIO

    @descfac        VARCHAR(100),
    @rutcli         VARCHAR(20),
    @tiposol        VARCHAR(50),
    @fechavisita    DATE, 
    @descsol        VARCHAR(100),
    @nrofac         INT,
    @idprod         INT, 
    @monto          INT,
    @estadogd       VARCHAR(50)
AS

BEGIN

    SET @nrofac = (SELECT MAX(nrofac) + 1 FROM FACTURA)

    INSERT INTO Factura(nrofac,rutcli,idprod,fechafac, descfac,monto)
    VALUES (
        @nrofac,
        @rutcli,

        CASE WHEN @tiposol = 'Instalación' THEN @idprod ELSE 1 END,

        GETDATE(),
        @descfac,
        CASE WHEN @tiposol = 'Instalación' THEN @monto ELSE 25000 END

    )

    IF (tiposol = 'Instalación')
    BEGIN
        INSERT INTO GuiaDespacho (nrogd, estadogd, idprod, nrofac)
        VALUES(
            (SELECT ISNULL(MAX(nrogd), 0) + 1 FROM GuiaDespacho),
            'En bodega',
            CASE WHEN @tiposol = 'Instalación' THEN @idprod ELSE 3 END,
            @nrofac

        )

        END


    INSERT INTO SolicitudServicio(nrosol, tiposol,fechavisita,descsol,estadosol,nrofac,ruttec)
    VALUES(
        (SELECT ISNULL(MAX(nrosol), 0) + 1 FROM SolicitudServicio),
        @tiposol,
        @fechavisita,
        @descsol,
        'Aceptada',
        @nrofac,
        '6666-6'
        
    )

    END



